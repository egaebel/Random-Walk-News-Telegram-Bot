from time import sleep

import httplib2
import json
import urllib.parse

CACHE_DIR = "cache"
TELEGRAM_API_BASE_URL = "https://api.telegram.org/bot"

class TelegramBot():
    def __init__(self, bot_token_file_path, message_read_delay=5):
        self.http = httplib2.Http(CACHE_DIR, ca_certs="/etc/ssl/certs/ca-certificates.crt")
        self.bot_token = self._read_bot_token(bot_token_file_path)
        self.message_read_delay = message_read_delay

    def _read_bot_token(self, bot_token_file_path):
        with open(bot_token_file_path, "r") as bot_token_file:
            bot_token = bot_token_file.read().strip()
        return bot_token

    def _get_method_endpoint(self, method_name):
        return TELEGRAM_API_BASE_URL + self.bot_token + "/" + method_name

    def update_loop(self, action_function):
        offset = None
        while True:
            try:
                get_updates_body = {"offset": offset}
                updates = self.get_updates(body=get_updates_body)
                results = updates["result"]
                if len(results) > 0:
                    offset = max(map(lambda x: x["update_id"], updates["result"])) + 1
                    print("%d results obtained!" % len(results))
                for update in results:
                    response_bodies = action_function(update)
                    for response_body in response_bodies:
                        self.send_message(response_body)    
            except Exception as e:
                print("ERROR: Exception caught.\n%s" % str(e))
            sleep(self.message_read_delay)

    def get_me(self):
        return self.make_get_request(self._get_method_endpoint("getMe"))

    def send_message(self, body):
        return self.make_get_request(self._get_method_endpoint("sendMessage"), body)

    def get_updates(self, body=dict()):
        return self.make_get_request(self._get_method_endpoint("getUpdates"), body)

    def make_get_request(self, base_url, body={}, headers={}):
        print("\nmake_get_request call:")
        print("Making get request to url: %s" % base_url)
        url_encoded_body = urllib.parse.urlencode(body.copy())
        print("Body: %s" % url_encoded_body)
        full_url = base_url + "?" + url_encoded_body\
            if len(body) != 0\
            else base_url
        print("Full request: %s" % full_url)
        response, content = self.http.request(
            full_url,
            "GET",
            headers=headers)
        print("Response: %s" % response)
        if response["status"] != "200":
            print("Content: %s" % content.decode("utf-8"))

        print("\n")
        return json.loads(content.decode("utf-8")) 


if __name__ == '__main__':
    bot = TelegramBot()
    
    response = bot.get_me()
    print(response)

    response = bot.send_message({"chat_id": -211817791, "text": "Hi this worked"})
    print(response)

    def test_action_fn(update):
        print("Message:\n%s" % update)
        message = update["message"]
        chat = message["chat"]
        chat_id = chat["id"]
        text = message["text"]

        if text == "/start":
            return [{
                "chat_id": chat_id,
                "text": "You sent start, lets get started."
            }]
        else:
            return [{
                "chat_id": chat_id,
                "text": "You said '%s' I don't know wtf that means..." % text
            }]

    bot.update_loop(test_action_fn)