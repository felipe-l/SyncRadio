from flask import Flask, jsonify, send_file, send_from_directory, request
import time
import threading
import os
from mutagen.mp3 import MP3
import random

app = Flask(__name__)

GENRES = ['techno', 'house', 'ava', 'jrock']
SONGS_DIR = 'songs'
SONGS = {genre: [f for f in os.listdir(os.path.join(SONGS_DIR, genre)) if f.endswith('.mp3')] for genre in GENRES}

#Shuffle all songs
for list_of_songs in SONGS.values():
    random.shuffle(list_of_songs)

SONG_DURATIONS = {genre: {} for genre in GENRES}

# Dictionary to store active listeners
active_listeners = {genre: {} for genre in GENRES}

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
                #print("UPDATING", self.genre, self.current_song_index, self.current_time, SONG_DURATIONS[self.genre][SONGS[self.genre][self.current_song_index]])
                if self.current_time >= SONG_DURATIONS[self.genre][SONGS[self.genre][self.current_song_index]]:
                    #print("CHANGING SONG", self.genre)
                    self.current_song_index = (self.current_song_index + 1) % len(SONGS[self.genre])
                    self.current_time = 0
            time.sleep(1)

players = {genre: MusicPlayer(genre) for genre in GENRES}

def load_song_durations():
    for genre in GENRES:
        for song in SONGS[genre]:
            audio = MP3(os.path.join(SONGS_DIR, genre, song))
            SONG_DURATIONS[genre][song] = int(audio.info.length)

# Function to clean up inactive listeners
def cleanup_listeners():
    while True:
        current_time = time.time()
        for genre in GENRES:
            active_listeners[genre] = {id: last_active for id, last_active in active_listeners[genre].items() if current_time - last_active < 60}
        time.sleep(60)  # Run every 60 seconds

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
    if genre not in GENRES and genre not in ["charly","hbd","msweets"]:
        return "Genre not found", 404
    print("SENDING TO ", genre)
    return send_from_directory('static', f'{genre}.html')
    
@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<genre>/heartbeat')
def heartbeat(genre):
    genre = genre.lower()
    if genre not in GENRES:
        return "Genre not found", 404
    
    listener_id = request.headers.get('X-Forwarded-For')  # Use IP address as listener ID from AWS header
    active_listeners[genre][listener_id] = time.time()
    print("HERE", active_listeners[genre])
    return "OK"

@app.route('/<genre>/listener_count')
def listener_count(genre):
    genre = genre.lower()
    if genre not in GENRES:
        return "Genre not found", 404
    
    count = len(active_listeners[genre])
    print("SENDING COUNT")
    return jsonify({"count": count})

if __name__ == '__main__':
    load_song_durations()
    
    # Start the background threads
    for player in players.values():
        bg_thread = threading.Thread(target=player.update, daemon=True)
        bg_thread.start()
    
    # Start the background thread for cleanup
    cleanup_thread = threading.Thread(target=cleanup_listeners, daemon=True)
    cleanup_thread.start()
    
    app.run(host="0.0.0.0", port=5000, debug=True)
