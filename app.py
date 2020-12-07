import os
from flask import Flask, render_template, request
import pymongo
from pymongo import MongoClient
import urllib.parse
from datetime import datetime

app = Flask(__name__)

MONGO_URI = str(os.environ.get('MONGO_URI'))
mongo = MongoClient(MONGO_URI)

from pymongo.errors import BulkWriteError

from random import randrange
from src.web_functions import get_quote, pick_random_from_array, get_grammatical_quote_from_input, get_any_quote_from_input, get_grammatical_quote_from_input_array

from flask_cors import CORS, cross_origin
# public API, allow all requests *
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from bs4 import BeautifulSoup
import requests

from dotenv import load_dotenv

from tweepy import Cursor
import tweepy

import glob

# pull quote from db.
@app.route('/')
def _main():
    quote="hey"
    return render_template('index.html', title='Home',quote=quote)

# generate shakespeare quote and add it to the db.
# takes a very long time...
@app.route('/generate-shakespeare')
def generate():
    is_logged_in = request.cookies.get('loggedin?')
    if is_logged_in == str(os.environ.get('is_logged_in')):
        db = mongo.db
        pregenerated_quotes = db.pregeneratedShakespeare

        read_filepath = "./public/data/tokenized_Shakespeare.md"
        quote = get_quote(read_filepath)
        new_quote_document = {"quote":quote}

        pregenerated_quotes.insert_one(new_quote_document)

        return render_template('index.html', quote=quote)
    else:
        return render_template('login.html')

# pull quote from db and return as JSON.
@app.route('/api/v1/quote',methods=['GET'])
@cross_origin()
def serve_quote():
    db = mongo.db
    pregenerated_quotes = db.pregeneratedShakespeare
    count = pregenerated_quotes.count()
    document = pregenerated_quotes.find()[randrange(count)]

    entry = {"quote":document["quote"],"author":document["author"]}

    return entry

# create quote from request.body and return as JSON.
@app.route('/api/v1/quote-from-input',methods=['POST'])
@cross_origin()
def serve_quote_from_input():
    data = request.get_json()
    if data:
        quote = get_grammatical_quote_from_input(data) # attempts to generate a grammatical quote first
        if not quote:
            quote = get_any_quote_from_input(data) # generates any sequence
        return {"quote": quote}
    else:
        return {"quote": "lol"}

# create quote from tweets associated a twitter handle and return as JSON.
@app.route('/api/v1/quote-from-twitter-handle',methods=['POST'])
@cross_origin()
def serve_quote_from_twitter():
    handle = request.get_json()
    if len(handle)>1:
        if handle[0] == "@":
            handle = handle[1:]
    words_from_tweets = []
    db = mongo.db
    collection = db.tweeters
    entry = collection.find_one({"handle":handle})
    if entry:
        entry_year, entry_month, entry_day = entry["timestamp"].split(" ")[0].split("-")[:3]
        today_year, today_month, today_day = str(datetime.now()).split(" ")[0].split("-")[:3]
        elapsed_years = int(today_year) - int(entry_year)
        elapsed_months = int(today_month) - int(entry_month)
        elapsed_days = int(today_day) - int(entry_day)
        elapsed_year_in_days = elapsed_years * 30 * 12
        elapsed_month_in_days = elapsed_months * 30
        elapsed_days += elapsed_year_in_days + elapsed_month_in_days
        if elapsed_days < 30:
            words_from_tweets = entry["words"]
        else:
            auth = tweepy.OAuthHandler(os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_API_SECRET"))
            auth.set_access_token(os.environ.get("TWITTER_ACCESS_TOKEN_KEY"), os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"))
            api = tweepy.API(auth)
            tweet_content = []

            tweet_count = 0
            for status in Cursor(api.user_timeline, id=handle).items():
              tweet_count += 1
              if hasattr(status, "text"):
                text = status.text
                tweet_content.append(text)
              if tweet_count > 1000:
                  break
            forbidden = set(['@','#','&','…'])
            for tweet in tweet_content:
                word = []
                for char in tweet:
                    if char == " ":
                        if len(word):
                            new_word = "".join(word)
                            words_from_tweets.append(new_word)
                            word = []
                    else:
                        if char not in forbidden:
                            word.append(char)
                        else:
                            word = []
            print(words_from_tweets)
            if words_from_tweets:
                new_document = {"handle":handle, "words": words_from_tweets, "timestamp": str(datetime.now())}
                collection.find_one_and_delete( {"handle":handle} )
                collection.insert_one(new_document)
                print("updating DB")
    else:
        auth = tweepy.OAuthHandler(os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_API_SECRET"))
        auth.set_access_token(os.environ.get("TWITTER_ACCESS_TOKEN_KEY"), os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"))
        api = tweepy.API(auth)
        tweet_content = []

        tweet_count = 0
        for status in Cursor(api.user_timeline, id=handle).items():
          tweet_count += 1
          if hasattr(status, "text"):
            text = status.text
            tweet_content.append(text)
          if tweet_count > 1000:
              break
        forbidden = set(['@','#','&','…'])
        for tweet in tweet_content:
            word = []
            for char in tweet:
                if char == " ":
                    if len(word):
                        new_word = "".join(word)
                        words_from_tweets.append(new_word)
                        word = []
                else:
                    if char not in forbidden:
                        word.append(char)
                    else:
                        word = []
        new_document = {"handle":handle, "words": words_from_tweets, "timestamp": str(datetime.now())}
        collection.insert_one(new_document)
    if words_from_tweets:
        quote = get_grammatical_quote_from_input_array(words_from_tweets)
    else:
        quote = "out of service"
    return {"quote": quote}

# create quote from url content and return as JSON.
@app.route('/api/v1/quote-from-url',methods=['POST'])
@cross_origin()
def serve_quote_from_url():
    url = request.get_json()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    p_array = soup.find_all("p")
    pre_array = soup.find_all("pre")
    data = p_array + pre_array
    if data:
        for i in range(len(data)):
            stack = 0
            entry = []
            data[i] = data[i].prettify()
            for c in data[i]:
                if c == "<":
                    stack+=1
                elif c == ">":
                    stack-=1
                elif not stack:
                    entry.append(c)
            data[i] = "".join(entry)
    else:
        data = soup.get_text().split(" ")
    if data:
        quote = get_grammatical_quote_from_input_array(data)
    else:
        quote = ""
    return {"quote": quote}

# get a random handle from the database.
@app.route('/api/v1/rand-handle',methods=['GET'])
@cross_origin()
def get_handle_in_database():
    db = mongo.db
    collection = db.tweeters
    _count = collection.count()
    handle = collection.find()[randrange(_count)]["handle"]
    return {"handle": handle}

@app.route('/api/v1/tweet',methods=['POST'])
@cross_origin()
def tweet():
    req = request.get_json()
    print(req)

    tweet = req["tweet"]
    handle = req["handle"]

    if len(handle)>1:
        if handle[0] == "@":
            handle = handle[1:]

    print(tweet,handle)

    db = mongo.db
    collection = db.tweeters
    entry = collection.find_one({"handle":handle})
    print(entry.get("handle",False))
    # check to make sure that the content of the tweet recieved from the frontend
        # is valid, by checking the words of the tweet with the words in the database
        # for that user
    if entry:
        unique_words_from_twitter_user = set(entry["words"])
        words_of_tweet = tweet.split(" ")
        for word in words_of_tweet:
            if word not in unique_words_from_twitter_user:
                return {"err":"Invalid tweet."}
    else:
        return {"err":"Invalid handle."}

    auth = tweepy.OAuthHandler(os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_API_SECRET"))
    auth.set_access_token(os.environ.get("TWITTER_ACCESS_TOKEN_KEY"), os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"))
    api = tweepy.API(auth)
    status = tweet + " @" + handle
    # this doesn't seem to work all of the time...
    api.update_status(status)
    return {"status":status}

if __name__ == '__main__':
    port = os.getenv("PORT", 7000)
    app.run(host = '0.0.0.0', port = int(port), debug=True)
    # app.run() // might need this if heroku doesn't want me to specify the port.
