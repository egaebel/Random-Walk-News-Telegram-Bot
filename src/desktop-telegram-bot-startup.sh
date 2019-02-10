#!/bin/bash

echo "Killing prior runs..."
pkill -f random_walk_news_bot.py

startup_time="$(date +%s)"

cd /home/egaebel/workspace/Programs/candlelight-experiments/random-walk-news-telgram-bot/src

source ../bin/activate

echo "Running new instance of random_walk_news_bot.py"
python random_walk_news_bot.py &> random-walk-news-bot-"$startup_time".log &

deactivate
