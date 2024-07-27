import json
import os
from PoemCollector import PoemCollector
from PoemService import PoemService
from TelegramBot import TelegramBot

if __name__ == "__main__":
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

  
    collector = PoemCollector(config)
    collector.collect_poem_ids()

    service = PoemService(config)

    poem_details, error = service.fetch_random_poem()
    
    if poem_details:
        message = f"***{poem_details['fullTitle']}***\n\n{poem_details['plainText']}\n\n[گنجور](https://ganjoor.net{poem_details['fullUrl']})\n📍@{config['channel_id_text']}"
        
        telegram_bot = TelegramBot(config)
        response = telegram_bot.send_message(message)
        print("Message sent to Telegram:", response)
    else:
        print("Error:", error)
