#!/bin/bash

startup_time="$(date +%s)"

cd /home/egaebel/workspace/Programs/candlelight-experiments/random-walk-news-telgram-bot/src

source ../bin/activate

python random_walk_news_bot.py &> random-walk-news-bot-"$startup_time".log &

deactivate
