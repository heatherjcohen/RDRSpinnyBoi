
from __future__ import with_statement
import pandas as pd
from datetime import datetime
import contextlib

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

import sys, random, tweepy, json, os
import numpy as np

CONSUMER_KEY = os.environ["TWITTER_API_CKEY"]
CONSUMER_SECRET = os.environ["TWITTER_API_CSECRET"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_SECRET"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

print(CONSUMER_KEY)

def get_recommendations(url, columns):
    df = pd.read_csv(url, header=None, names=columns)

    #add tiny links
    def make_tiny(url_list):
        tiny_column = []
        for url in url_list:
            tiny_column.append(tiny(url))
        df['Tiny'] = tiny_column

    def tiny(url):
        request_url = ("http://tinyrl.com/api-create.php?" + urlencode({"url":url}))
        with contextlib.closing(urlopen(request_url)) as response:
            return response.read().decode('utf-8')

    make_tiny(df['Link'])
    return df

spinnydf = get_recommendations("https://docs.google.com/spreadsheets/d/e/2PACX-1vTWc2VxHamAlR4RQK2GiDg6eVGiWa-azbIssCeSwxMnOOuqv200oZoIgxF4LWcAWHOAVBugXLUbQx9E/pub?output=csv", ['Title', "Genre", "Genre Number", "Link"])

def spin_the_wheel(df):
    spin = random.randint(1, 12)
    spin2 = random.randint(0, len(df[df['Genre Number'] == spin]))
    winner = df[df['Genre Number'] == spin].iloc[spin2]
    winner['Title'] = winner['Title'].title()
    winner['Genre'] = winner['Genre'].title()

    return winner

Win = spin_the_wheel(spinnydf)

Tweets = pd.DataFrame()

def get_mentions(n):
    df = pd.DataFrame(columns=['Tweet ID', 'User', 'Created At', 'Text'])
    result_list = api.mentions_timeline(count=n)
    for i in range(len(result_list)):
        json_str = json.dumps(status._json)
        text = json.loads(json_str)
        twitter_user = text['user']['screen_name']
        tweet_id = text['id']
        tweet_time = text['created_at']
        tweet_text = text['text']
        data = {'Tweet ID': tweet_id, "User": twitter_user, "Created At": tweet_time, "Text": tweet_text}

        df = df.append(data, ignore_index=True)

    return df

def reply_and_update(Win, history, now, new, not_replied_to):
    if len(not_replied_to) > 0:
        for tweet, idx in enumerate(not_replied_to):
            print("I am responding to tweet #: " + str(idx + 1))
            api.update_status(f"@{not_replied_to['User'][idx]} You got {Win['Genre']}. Why not try out {Win['Title']}? This podcast can be found at {Win['Tiny']}", not_replied_to['Tweet ID'][idx])
            history = history.append(not_replied_to, ignore_index=True)
            history.loc[history['Tweet ID'] == not_replied_to['Tweet ID'][idx], 'Responded'] = 'Yes'
            history.to_csv('history.csv')

    else:
        print("Nothing to respond to")

def do_the_thing():
    a_winner = spin_the_wheel(spinnydf)
    Tweets = pd.Dataframe()
    now = get_mentions(50)
    history = pd.read_csv('history.csv')
    new = np.setdiff1d(now['Tweet ID'], history['Tweet ID'])
    not_replied_to = now[now['Tweet ID'].isin(new)]
    
    reply_and_update(a_winner, history, now, new, not_replied_to)

#AT THIS POINT, ADD EITHER:
# - a single call to do_the_thing() that will be run each time a cron job triggers this script
# OR
# - a continuously running server thing that periodically polls twitter and responds to new shit
#   on the fly
