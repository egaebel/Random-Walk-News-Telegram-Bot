from telegram_bot import TelegramBot

import httplib2
import json
import urllib.parse

class RandomWalkNewsBot(TelegramBot):
    def __init__(self):
        TelegramBot.__init(self)

if __name__ == '__main__':
    bot = RandomWalkNewsBot()
    
    response = bot.get_me()
    print(response)

    response = bot.send_message(-211817791, "Hi this worked")
    print(response)

    response = bot.get_updates()
    print(response)
    for update in response["result"]:
        message = update["message"]
        # Ignore other bots
        if message["from"]["is_bot"]:
            continue

        if message["text"] == "/news":
            # Run random walk news and send the urls in a message
            # Then make it pretty :)
            bot.send_message
