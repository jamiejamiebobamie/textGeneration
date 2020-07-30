import os
from flask import Flask, render_template, request
import pymongo
from pymongo import MongoClient
import urllib.parse
# MONGO_URL = os.environ.get('MONGO_URL')
# if not MONGO_URL:
#     MONGO_URL = "mongodb://localhost:27017/rest";
app = Flask(__name__)
# app.config['MONGO_URI'] = MONGO_URL
# MONGO_URI = str(os.environ.get('MONGO_URI2'))
# MONGO_URI = None
# if not MONGO_URI:
    # MONGO_URI = "mongodb://localhost:27017/rest";
#
# user = os.environ.get('HEROKU_USER')
# password = os.environ.get('HEROKU_PASSWORD')
# user = urllib.parse.quote_plus(str(user))
# password = urllib.parse.quote_plus(str(password))
# host = os.environ.get('HEROKU_HOST')
# database = os.environ.get('HEROKU_DATABASE')
# host = urllib.parse.quote_plus(str(host))
# database = urllib.parse.quote_plus(str(database))

MONGO_URI = str(os.environ.get('MONGO_URI3'))
mongo = MongoClient(MONGO_URI)


# mongo = MongoClient('mongodb://%s:%s@%s/%s?retryWrites=false' % (user, password, host, database))

# mongo = MongoClient(MONGO_URI)

# from urlparse import urlsplit
# MONGO_URL = os.getenv('MONGODB_URI')
# parsed = urlsplit(url)
# db_name = parsed.path[1:]
# app.config['MONGO_URI'] = MONGO_URL
# import pymongo
# # from pymongo import pymongo, MongoClient#, Connection
# # client = pymongo.MongoClient(os.getenv(“MONGODB_URI”, “mongodb://127.0.0.1:27017/database”))
# # client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
# client = pymongo.MongoClient(os.getenv("MONGO_URL", "mongodb://127.0.0.1:27017/database"))

from random import randrange
from src.web_functions import get_quote, pick_random_from_array, get_grammatical_quote_from_input, get_any_quote_from_input, get_grammatical_quote_from_input_array
from src.Quote_document import Quote

from flask_cors import CORS, cross_origin
# public API, allow all requests *
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from bs4 import BeautifulSoup
import requests

from dotenv import load_dotenv

from tweepy import Cursor
import tweepy


# pull quote from db.
@app.route('/')
def _main():
    # db = client.database
    # quotes_collection = db.quotes
    # count = quotes_collection.count()
    # quote = quotes_collection.find()[randrange(count)]["quote"]
    quote = "hey jamie. i love you."
    # # new code using mongoengine python plugin
    # quote_document = quotes_collection.find()[randrange(count)]
    # quote = quote_document.quote

    return render_template('index.html', title='Home',quote=quote)


# pull quote from db.
@app.route('/testDB')
def test_DB():
    words_from_tweets = []

    db = mongo.db
    collection = db.tweeters
    # print(db.name, collection.name)
    # print(collection.count())
    # quote = str(collection.count())
    # quote = quotes_collection.find()[randrange(count)]["quote"]

    handle = 'BarackObama'
    entry = collection.find_one({"handle":handle})
    if entry:
        words_from_tweets = entry["words"]
        print("pulling from DB")
    else:
        if len(handle)>1:
            if handle[0] == "@":
                handle = handle[1:]

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
          if tweet_count > 2000:
              break

        # words_from_tweets = []
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

        new_document = {"handle":handle, "words": words_from_tweets}
        collection.insert_one(new_document)
        print("inserting to DB")

    if words_from_tweets:
        quote = get_grammatical_quote_from_input_array(words_from_tweets)
    else:
        quote = "out of service"

    # return {"quote": quote}

    # ------

    # # new code using mongoengine python plugin
    # quote_document = quotes_collection.find()[randrange(count)]
    # quote = quote_document.quote
    # quote = "out of service"

    return render_template('index.html', title='Home',quote=quote)

# add quote to db.
@app.route('/generate')
def generate():
    read_filepath = "./public/data/tokenized_Shakespeare.md"
    quote = get_quote(read_filepath)
    new_quote_document = {"quote":quote}

    # new code using mongoengine python plugin

    # new_quote_document = Quote()
    # new_quote_document.quote = quote
    # db = client.database
    # quotes_collection = db.quotes
    # quotes_collection.insert_one(new_quote_document)
    return render_template('index.html', title='Home',quote=quote)

# pull quote from file.
@app.route('/pregenerated')
def pregenerated():
    file = 'src/quotes_tokenized_Shakespeare.md'
    quotes = []
    with open(file, "r") as pregenerated_quotes:
        for line in pregenerated_quotes:
            quotes.append(line)
    quote = pick_random_from_array(quotes)
    return render_template('index.html', title='Home',quote=quote)

# pull quote from db and return as JSON.
@app.route('/api/v1/quote',methods=['GET'])
@cross_origin()
def serve_quote():
    db = client.database
    quotes_collection = db.quotes
    count = quotes_collection.count()
    quote = quotes_collection.find()[randrange(count)]
    return {"quote": quote["quote"]}

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

    db = mongo.db
    collection = db.tweeters
    entry = collection.find_one({"handle":handle})
    if entry:
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
          if tweet_count > 2000:
              break
        words_from_tweets = []
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

# create quote from tweets associated a twitter handle and return as JSON.
@app.route('/api/v1/quote-from-author',methods=['POST'])
@cross_origin()
def serve_quote_from_file():
    authorName = request.get_json()

    file = 'src/quotes_tokenized_Shakespeare.md'
    quotes = []
    with open(file, "r") as pregenerated_quotes:
        for line in pregenerated_quotes:
            quotes.append(line)
    quote = pick_random_from_array(quotes)
    # grimm rowling and shakespeare
    # read_filepath = "./public/data/tokenized_Shakespeare.md"
    # quote = get_quote(read_filepath)
    return {"quote": quote}

if __name__ == '__main__':
    port = os.getenv("PORT", 7000)
    app.run(host = '0.0.0.0', port = int(port), debug=True)
    # app.run() // might need this if heroku doesn't want me to specify the port.
