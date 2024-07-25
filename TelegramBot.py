import requests

class TelegramBot:
    def __init__(self, config):
        self.bot_token = config["bot_token"]
        self.chat_id = config["channel_id_numeric"]

    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview":True
        }
        response = requests.post(url, data=payload)
        return response.json()
