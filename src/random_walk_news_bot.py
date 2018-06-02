import sys
sys.path.insert(1, "../../random-walk-news/src")
print("Path: %s" % sys.path)
from news_api import NewsApi
from news_api import get_domains

from telegram_bot import TelegramBot

import httplib2
import json
import re
import urllib.parse

class RandomWalkNewsBot(TelegramBot):
    def __init__(self):
        TelegramBot.__init__(self)

def get_random_article_urls(num_articles):
    get_all_sources = False
    page_size = 100
    news_api = NewsApi()

    sources = None
    everything_body = {
        'sources': sources,
        'domains': ",".join(get_domains()),
        'language': 'en',
        'from': '2018-01-05',
        'sortBy': 'publishedAt',
        'pageSize': page_size,
    }
    random_article_urls = news_api.get_random_article_urls(
        everything_body, num_articles)

    domains_or_sources = get_domains() if sources is None else sources
    print("From sources/domains: %s\n\nGathered random urls:\n" 
        % "\n".join(domains_or_sources))
    print("\n".join([str(a) for a in random_article_urls]))

    return random_article_urls

def news_action(update):
    print("\n\nMessage:\n%s" % update)
    message = update["message"]
    chat = message["chat"]
    chat_id = chat["id"]
    text = message["text"]

    # Ignore other bots
    if message["from"]["is_bot"]:
        return

    if text.find("/start") == 0:
        return [{
            "chat_id": chat_id,
            "text": "You sent start, to get news type '/news'. To get other things, use other bots."
        }]
    elif text.find("/news") == 0:
        num_articles = 1
        print("text: ||%s||" % text)
        print("re fullmatch result: %s" % str(re.fullmatch(text, "/news [0-9]+")))
        if re.fullmatch("^/news [0-9]+$", text) is not None:
            num_articles = int(text.split()[1])
            print("Set num articles to: %d " % num_articles)
        # Run random walk news and send the urls in a message
        # Then make it pretty :)
        return [{
            "chat_id": chat_id,
            "text": "%s" % random_article_url,
        }
        for random_article_url in get_random_article_urls(num_articles)]
    else:
        return [{
            "chat_id": chat_id,
            "text": "I only know \"/news\". Do you want news? PLEASE TELL ME YOU WANT NEWS!?",
        }]

if __name__ == '__main__':
    bot = RandomWalkNewsBot()

    bot.update_loop(news_action)


