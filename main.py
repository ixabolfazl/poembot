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
        import html
        poet_nickname_hashtag = ""
        if poem_details.get('poet_nickname'):
            poet_nickname = poem_details['poet_nickname']
            poet_nickname_hashtag = f"#{poet_nickname.replace(' ', '_')} | "
            poet_nickname_hashtag = html.escape(poet_nickname_hashtag)

        title = html.escape(poem_details['fullTitle'])
        plain_text = html.escape(poem_details['plainText'])
        full_url = html.escape(poem_details['fullUrl'])
        channel_id_text = html.escape(config['channel_id_text'])

        message = f"<b>{title}</b>\n\n{plain_text}\n\n{poet_nickname_hashtag}<a href=\"https://ganjoor.net{full_url}\">گنجور</a>\n📍@{channel_id_text}"
        
        telegram_bot = TelegramBot(config)
        response = telegram_bot.send_message(message)
        print("Message sent to Telegram:", response)
    else:
        print("Error:", error)
