from multiprocessing.connection import wait
from TwitterAPI import TwitterAPI
from threader import Threader
import re, os
from dotenv import load_dotenv
import time
load_dotenv()
h = os.getenv('HASH_TAGS')
hashtags = os.getenv('HASH_TAGS').split('|')
hello=2
def retweet(api, tweet_id):
    r = api.request('')
def get_tweets(api, query, output_file):
    r = api.request('tweets/search/recent', {
        'query': query,
        'tweet.fields':'author_id',
		'expansions':'author_id'
        })
    lines = []
    with open(output_file, 'a') as file:
        for item in r:
            text = item['text'].split('\n')[0]
            for h in hashtags:
                text.replace(h, '')
            text = re.sub(r"[a-zA-Z0-9|^[:punct:]|\/|\@]*", "", text)
            # print(text)
            file.write(text + "\n")
            lines.append(text)
    file.close()
    return lines

keys = dict(consumer_key=os.getenv('CONSUMER_KEY'),
            consumer_secret=os.getenv('CONSUMER_SECRET'),
            access_token_key=os.getenv('ACCESS_TOKEN_KEY'),
            access_token_secret=os.getenv('ACCESS_TOKEN_SECRET'),
            api_version='2')
api = TwitterAPI(**keys)
filename= 'tweets.txt'
tags = " ".join(hashtags)
# with open(filename) as file:
#     lines = file.readlines()
#     lines = [f" {line.rstrip()} {tags}"  for line in lines]
while True:
    lines = get_tweets(api, os.getenv('SEARCH_KEYWORD'), 'new_tweets.txt')
    lines = [f" {line.rstrip()} {tags}"  for line in lines]
    print(lines)
    th = Threader(lines, api, wait=2)
    th.send_tweets(indiviual=True)
    time.sleep(10)
