import json
import requests
import random
import os

class PoemService:
    def __init__(self, config):
        self.input_file_path = config["poem_ids_file"]
        self.poem_ids_dict = self.load_poem_ids()

    def load_poem_ids(self):
        if os.path.exists(self.input_file_path):
            with open(self.input_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}

    def fetch_random_poem(self):
        false_poem_ids = [poem_id for poem_id, status in self.poem_ids_dict.items() if status is False]
        if not false_poem_ids:
            return None, "No IDs with a value of false found."
        
        random_poem_id = random.choice(false_poem_ids)
        return self.get_poem_details(random_poem_id)

    def get_poem_details(self, poem_id):
        url = f'https://api.ganjoor.net/api/ganjoor/poem/{poem_id}?catInfo=false&catPoems=false&rhymes=false&recitations=false&images=false&songs=false&comments=false&verseDetails=false&navigation=false&relatedpoems=false'
        response = requests.get(url)

        if response.status_code == 200:
            poem_data = response.json()
            poem_details = {
                "title": poem_data.get('title', 'Unknown'),
                "fullTitle": poem_data.get('fullTitle', 'Unknown').replace('»', '|'),
                "fullUrl": poem_data.get('fullUrl', 'Unknown'),
                "plainText": poem_data.get('plainText', 'Unknown'),
                "htmlText": poem_data.get('htmlText', 'Unknown')
            }

            self.poem_ids_dict[str(poem_id)] = True
            self.save_poem_ids()

            return poem_details, None
        else:
            return None, f"Error fetching data for poem {poem_id}: {response.status_code}"

    def save_poem_ids(self):
        with open(self.input_file_path, 'w', encoding='utf-8') as file:
            json.dump(self.poem_ids_dict, file, ensure_ascii=False, indent=4)
