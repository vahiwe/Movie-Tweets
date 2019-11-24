import tweepy
import pandas as pd
import requests
from os import getcwd
from datetime import datetime
from dateutil.parser import parse

# You need to insert your own developer twitter credentials here
consumer_key = ""
consumer_secret = ""
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)


# search_term = "spiderman"

def searching(term):
    tweets = tweepy.Cursor(api.search, q=term, lang='en',
                           count=20, tweet_mode='extended').items(20)

    dates = []
    stdates = []
    test = []
    users = []
    likes = []
    retweets = []
    for tweet in tweets:
        date = tweet.created_at
        date = parse(str(date))
        d = date.strftime("%c")
        like = tweet.favorite_count
        retweet = tweet.retweet_count
        status = tweet
        user = tweet._json['user']['screen_name']
        if 'extended_tweet' in status._json:
            status_json = status._json['extended_tweet']['full_text']
        elif 'retweeted_status' in status._json and 'extended_tweet' in status._json['retweeted_status']:
            status_json = status._json['retweeted_status']['extended_tweet']['full_text']
            like = status._json["retweeted_status"]["favorite_count"]
        elif 'retweeted_status' in status._json:
            status_json = status._json['retweeted_status']['full_text']
            like = status._json["retweeted_status"]["favorite_count"]
        else:
            status_json = status._json['full_text']
        test.append(status_json)
        dates.append(date)
        users.append(user)
        likes.append(like)
        retweets.append(retweet)
        stdates.append(d)

    df = pd.DataFrame(list(zip(test, dates, users, stdates, likes, retweets, likes)),
                      columns=["tweets", "dates", "users", "stdates", "likes", "retweets", "indie"])

    # df['dates'] = pd.to_datetime(df['dates'], format='%Y-%m-%d')
    df = df.drop_duplicates(subset='tweets', keep="first")
    df.set_index(['indie'], inplace=True)
    df.sort_index(inplace=True, ascending=False)

    return df


def getmovies():
    r = requests.get(
        "https://raw.githubusercontent.com/sidooms/MovieTweetings/master/latest/movies.dat")
    filename = 'movies.dat'
    f = open(filename, 'w')
    f.write(r.text)
    f.close()


def checkname(film):
    df = pd.read_csv('movies.dat', sep="::", header=None)
    df.columns = ['id', 'name', 'genre']
    df.drop(['id', 'genre'], axis=1, inplace=True)
    df['name'] = df['name'].str.replace(r" \(.*\)$", "")
    return df['name'].str.contains(film.lower(), case=False).any()
