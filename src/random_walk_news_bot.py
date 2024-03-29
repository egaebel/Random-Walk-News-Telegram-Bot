import sys
sys.path.insert(1, "../../random-walk-news/src")
print("Path: %s" % sys.path)
from news_api import NewsApi
from news_api import get_domains

from telegram_bot import TelegramBot

import datetime as dt
import httplib2
import json
import pytz
import re
import urllib.parse

MESSAGE_READ_DELAY = 3

RANDOM_NEWS_BOT_TOKEN_FILE_NAME = "RandomNewsBot--access-token.txt"
RNG_NEWS_BOT_TOKEN_FILE_NAME = "RngNewsBot--access-token.txt"
TIMEZONE = "America/Los_Angeles"
WALK_NEWS_BOT_TOKEN_FILE_NAME = "WalkNewsBot--access-token.txt"

class RandomNewsBot(TelegramBot):
    def __init__(self, bot_token_file_path):
        TelegramBot.__init__(self, bot_token_file_path, MESSAGE_READ_DELAY)

def get_domains_with_validation(news_api):
    return set(get_domains()).intersection(set(news_api.get_all_sources_urls()))

def get_random_article_urls(num_articles):
    get_all_sources = False
    page_size = 100
    news_api = NewsApi()

    sources = None
    everything_body = {
        'domains': ",".join(get_domains()),
        'language': 'en',
        'from': str(get_now().date()),
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

def get_now():
    return dt.datetime.now(pytz.timezone(TIMEZONE))

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
        random_article_urls_list = list()
        while len(random_article_urls_list) < num_articles:
            random_article_urls_list += (
                list(
                    filter(lambda x: not ("/sports/" in x or "/sport/" in x), 
                        get_random_article_urls(num_articles))))

        # Run random walk news and send the urls in a message
        # Then make it pretty :)
        return [{
            "chat_id": chat_id,
            "text": "%s" % random_article_url,
        }
        for random_article_url in get_random_article_urls(num_articles)]
    elif text.find("/sources") == 0:
        return [{
            "chat_id": chat_id,
            "text": "%s" % "\n".join(sorted(list(get_domains()))),
        }]
    elif text.find("/help") == 0:
        return [{
            "chat_id": chat_id,
            "text": "@randomwalknews provides recent news in a totally random fashion. "
                    "To get started send '/news' for a single news article, or /news N "
                    "to receive 'N' random news articles. Each news article is sent in "
                    "a separate message.",
        }]
    else:
        return [{
            "chat_id": chat_id,
            "text": "I only know \"/news\" and \"/sources\". Do you want news? PLEASE TELL ME YOU WANT NEWS!?",
        }]

if __name__ == '__main__':
    bot = RandomNewsBot(RNG_NEWS_BOT_TOKEN_FILE_NAME)

    bot.update_loop(news_action)


