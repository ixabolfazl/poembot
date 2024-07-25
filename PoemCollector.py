import json
import requests
import os

class PoemCollector:
    def __init__(self, config):
        self.output_file_path = config["poem_ids_file"]
        self.cat_ids = config["categories"]
        self.poem_ids_dict = self.load_poem_ids()

    def load_poem_ids(self):
        if os.path.exists(self.output_file_path):
            with open(self.output_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}

    def collect_poem_ids(self):
        for cat_id in self.cat_ids:
            url = f'https://api.ganjoor.net/api/ganjoor/cat/{cat_id}?poems=true&mainSections=false'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'cat' in data and 'poems' in data['cat']:
                    for poem in data['cat']['poems']:
                        poem_id = str(poem['id'])
                        if poem_id not in self.poem_ids_dict.keys():
                            self.poem_ids_dict[poem_id] = False
            else:
                print(f"Error fetching data for category {cat_id}: {response.status_code}")
        self.save_poem_ids()

    def save_poem_ids(self):
        with open(self.output_file_path, 'w', encoding='utf-8') as file:
            json.dump(self.poem_ids_dict, file, ensure_ascii=False, indent=4)
