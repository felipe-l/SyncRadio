from flask import Flask, jsonify, send_file, send_from_directory
import time
import threading
import os
from mutagen.mp3 import MP3
import random

app = Flask(__name__)

SONGS_DIR = 'songs'
SONGS = [f for f in os.listdir(SONGS_DIR) if f.endswith('.mp3')]
random.shuffle(SONGS)
SONG_DURATIONS = {}

class MusicPlayer:
    def __init__(self):
        self.current_song_index = 0
        self.current_time = 0
        self.lock = threading.Lock()

    def update(self):
        while True:
            with self.lock:
                self.current_time += 1
                if self.current_time >= SONG_DURATIONS[SONGS[self.current_song_index]]:
                    self.current_song_index = (self.current_song_index + 1) % len(SONGS)
                    self.current_time = 0
            time.sleep(1)

player = MusicPlayer()

def load_song_durations():
    for song in SONGS:
        audio = MP3(os.path.join(SONGS_DIR, song))
        SONG_DURATIONS[song] = int(audio.info.length)

@app.route('/current_song_info')
def current_song_info():
    with player.lock:
        current_song = SONGS[player.current_song_index]
        return jsonify({
            'songIndex': player.current_song_index,
            'currentTime': player.current_time,
            'totalTime': SONG_DURATIONS[current_song],
            'songName': current_song
        })

@app.route('/get_song/<int:index>')
def get_song(index):
    if 0 <= index < len(SONGS):
        return send_file(os.path.join(SONGS_DIR, SONGS[index]), mimetype="audio/mpeg")
    else:
        return "Song not found", 404

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/hello')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    load_song_durations()
    
    # Start the background thread
    bg_thread = threading.Thread(target=player.update, daemon=True)
    bg_thread.start()
    
    app.run(host="0.0.0.0", port=5000, debug=True)