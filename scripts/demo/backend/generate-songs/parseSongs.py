import json
import requests
import os
import sys
import uuid

if len(sys.argv) < 3:
    print("Please provide both arguments: genre and search_name")
    print("Expected format: python parseSongs.py <genre> <search_name>")
    sys.exit(1)

genre = sys.argv[1]
folder_name = f'songs/{genre}'
os.makedirs(folder_name, exist_ok=True)

search_name = sys.argv[2] #will be the suffix after songs-{THIS}.json

with open(f'songs-scrape/songs-{search_name}.json', 'r') as f:  # Changed 'sample-songs.json' to 'songs-scrape/songs-{sys.argv[1]}.json'
    songs_json = json.load(f)
    songs = songs_json['songs']
    start_index = 0
    end_index = len(songs)
    for i in range(start_index, end_index):
        audio_url = songs[i]["audio_url"]
        audio_name = f"{songs[i]['title'].strip()}_{uuid.uuid4().hex}"  # Include title in the audio name with a unique id after removing trailing whitespace
        display_name = f'{folder_name}/{audio_name}.mp3'
        response = requests.get(audio_url)
        with open(display_name, 'wb') as audio_file:
            audio_file.write(response.content)
        print(f"Downloaded: {display_name}")
