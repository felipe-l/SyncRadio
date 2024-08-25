from flask import Flask, jsonify, send_file, send_from_directory
import time
import threading
import os
from mutagen.mp3 import MP3
import random

app = Flask(__name__)

GENRES = ['techno', 'house', 'ava']
SONGS_DIR = 'songs'
SONGS = {genre: [f for f in os.listdir(os.path.join(SONGS_DIR, genre)) if f.endswith('.mp3')] for genre in GENRES}

#Shuffle all songs
for list_of_songs in SONGS.values():
    random.shuffle(list_of_songs)

SONG_DURATIONS = {genre: {} for genre in GENRES}

class MusicPlayer:
    def __init__(self, genre):
        self.genre = genre
        self.current_song_index = 0
        self.current_time = 0
        self.lock = threading.Lock()

    def update(self):
        while True:
            with self.lock:
                self.current_time += 1
                print("UPDATING", self.genre, self.current_song_index, self.current_time, SONG_DURATIONS[self.genre][SONGS[self.genre][self.current_song_index]])
                if self.current_time >= SONG_DURATIONS[self.genre][SONGS[self.genre][self.current_song_index]]:
                    print("CHANGING SONG", self.genre)
                    self.current_song_index = (self.current_song_index + 1) % len(SONGS[self.genre])
                    self.current_time = 0
            time.sleep(1)

players = {genre: MusicPlayer(genre) for genre in GENRES}

def load_song_durations():
    for genre in GENRES:
        for song in SONGS[genre]:
            audio = MP3(os.path.join(SONGS_DIR, genre, song))
            SONG_DURATIONS[genre][song] = int(audio.info.length)

@app.route('/<genre>/current_song_info')
def current_song_info(genre):
    genre = genre.lower()
    if genre not in GENRES:
        return "Genre not found", 404
    player = players[genre]
    with player.lock:
        current_song = SONGS[genre][player.current_song_index]
        return jsonify({
            'songIndex': player.current_song_index,
            'currentTime': player.current_time,
            'totalTime': SONG_DURATIONS[genre][current_song],
            'songName': current_song
        })

@app.route('/<genre>/get_song/<int:index>')
def get_song(genre, index):
    genre = genre.lower()
    if genre not in GENRES:
        return "Genre not found", 404
    if 0 <= index < len(SONGS[genre]):
        return send_file(os.path.join(SONGS_DIR, genre, SONGS[genre][index]), mimetype="audio/mpeg")
    else:
        return "Song not found", 404

@app.route('/<genre>')
def serve_genre_index(genre):
    genre = genre.lower()
    if genre not in GENRES and genre != "charly":
        return "Genre not found", 404
    print("SENDING TO ", genre)
    return send_from_directory('static', f'{genre}.html')
    
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    load_song_durations()
    
    # Start the background threads
    for player in players.values():
        bg_thread = threading.Thread(target=player.update, daemon=True)
        bg_thread.start()
    
    app.run(host="0.0.0.0", port=5000, debug=True)
