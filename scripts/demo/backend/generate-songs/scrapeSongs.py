import requests
import json
import time
import random
import sys
import os
from dotenv import load_dotenv
from config import search_config 
from getToken import refreshToken

if len(sys.argv) != 2:
    print("Please provide one argument: <search_name>")
    print("Example: python test.py techno")
    sys.exit(1)


#load env variables
load_dotenv()

# Retrieve the Bearer token
bearer_token = os.getenv('BEARER_TOKEN')

# Define the URL
url = "https://studio-api.suno.ai/api/search/"

# Define the headers
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.5",
    "affiliate-id": "undefined",
    "authorization": f"{bearer_token}",
    "content-type": "text/plain;charset=UTF-8",
    "origin": "https://suno.com",
    "priority": "u=1, i",
    "referer": "https://suno.com/",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

songs_json = {}
for i in range(0,6):
    if search_config['search_type'] == "public_song":
        headers["authorization"] = f"Bearer {refreshToken()}"
    data = {
        "search_queries": [
            {
                "name": search_config['name'],
                "search_type": search_config['search_type'],
                "term": search_config['term'], # "term": "rap, pop",
                "from_index": 20*i,
                "rank_by": search_config['rank_by'] #'msg': "Input should be 'upvote_count', 'play_count', 'dislike_count', 'trending', 'most_recent', 'most_relevant', 'by_day', 'by_week', 'by_month', 'all_time' or 'default'"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    folder_name = f'multi-data/songs-{sys.argv[1]}'  # set arg1 to the first argument passed when calling the script
    os.makedirs(folder_name, exist_ok=True)
    with open(f'{folder_name}/sample-search-{i}.json', 'w') as f:
        json.dump(response.json(), f)
    
    songs_data = response.json()['result']['tag_song']['result']
    
    if response.json()['result']['tag_song']['total_hits'] == 0:
        print(f"Ran out at when searching after {i*20}!")
        sys.exit(1)

    if i == 0:
        songs_json = {
            "name": data['search_queries'][0]['name'],
            "search_type": data['search_queries'][0]['search_type'],
            "term": data['search_queries'][0]['term'],
            "rank_by": data['search_queries'][0]['rank_by'],
            "checked_up_to": 0,
            "songs": songs_data
        }
    else:
        with open(f'songs-scrape/songs-{sys.argv[1]}.json', 'r') as f:
            existing_songs_json = json.load(f)
        existing_songs_json['songs'].extend(songs_data)
        existing_songs_json["checked_up_to"] = (i+1)*20
        songs_json = existing_songs_json

    with open(f'songs-scrape/songs-{sys.argv[1]}.json', 'w') as f:  # Changed 'w' to 'a' to append to the file
        json.dump(songs_json, f)

    print(response.status_code)
    time.sleep(random.randint(40, 70))

print("Success: Completed all iterations!")