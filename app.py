import os
from flask import Flask, render_template, request
app = Flask(__name__)

# from urlparse import urlsplit
MONGO_URL = os.getenv('MONGODB_URI')
# parsed = urlsplit(url)
# db_name = parsed.path[1:]
app.config['MONGO_URI'] = MONGO_URL
from pymongo import MongoClient#, Connection
client = MongoClient()

from random import randrange
from src.web_functions import get_quote, pick_random_from_array, get_grammatical_quote_from_input, get_any_quote_from_input, get_grammatical_quote_from_input_array
from src.Quote_document import Quote

from flask_cors import CORS, cross_origin
# public API, allow all requests *
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from bs4 import BeautifulSoup
import requests

from dotenv import load_dotenv
load_dotenv()

from tweepy import Cursor
import tweepy

from datetime import datetime, date, time, timedelta

# pull quote from db.
@app.route('/')
def _main():
    # db = client.database
    # quotes_collection = db.quotes
    # count = quotes_collection.count()
    # quote = quotes_collection.find()[randrange(count)]["quote"]
    quote = "quote"
    # # new code using mongoengine python plugin
    # quote_document = quotes_collection.find()[randrange(count)]
    # quote = quote_document.quote

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
    db = client.database
    quotes_collection = db.quotes
    quotes_collection.insert_one(new_quote_document)
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
        # print(quote)
        return {"quote": quote}
    else:
        return {"quote": "lol"}

# create quote from tweets associated a twitter handle and return as JSON.
@app.route('/api/v1/quote-from-twitter-handle',methods=['POST'])
@cross_origin()
def serve_quote_from_twitter():
# api = TwitterAPI(consumer_key,
#                  consumer_secret,
#                  access_token_key,
#                  access_token_secret)
    handle = request.get_json()
    if len(handle)>1:
        if handle[0] == "@":
            handle = handle[1:]

    auth = tweepy.OAuthHandler(os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_API_SECRET"))
    auth.set_access_token(os.environ.get("TWITTER_ACCESS_TOKEN_KEY"), os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"))
    api = tweepy.API(auth)

    # response = api.user_timeline(handle,{"count":200,"page":1})
    #
    tweet_content = []

    # https://blog.f-secure.com/how-to-get-tweets-from-a-twitter-account-using-python-and-tweepy/
    tweet_count = 0
    # end_date = datetime.utcnow() - timedelta(days=500)
    for status in Cursor(api.user_timeline, id=handle).items():
      tweet_count += 1
      # if hasattr(status, "entities"):
      #   entities = status.entities
      #   if "hashtags" in entities:
      #     for ent in entities["hashtags"]:
      #       if ent is not None:
      #         if "text" in ent:
      #           hashtag = ent["text"]
      #           if hashtag is not None:
      #             hashtags.append(hashtag)
      #   if "user_mentions" in entities:
      #     for ent in entities["user_mentions"]:
      #       if ent is not None:
      #         if "screen_name" in ent:
      #           name = ent["screen_name"]
      #           if name is not None:
      #             mentions.append(name)
      if hasattr(status, "text"):
        text = status.text
        tweet_content.append(text)
        # if "hashtags" in entities:
        #   for ent in entities["hashtags"]:
        #     if ent is not None:
        #       if "text" in ent:
        #         hashtag = ent["text"]
        #         if hashtag is not None:
        #           hashtags.append(hashtag)
      # if status.created_at < end_date:
      #   break
      if tweet_count > 5000:
          break

    # print(tweet_content)

    words_from_tweets = []
    forbidden = set(['@','#','&','…'])
    # count = 0
    for tweet in tweet_content:
        # if count > 30:
            # break
        word = []
        for char in tweet:
            # if count > 30:
            #     break
            # print(char)
            # count+=1
            if char == " ":
                if len(word):
                #     if word[0] != "@" and word[0] != "#" and word[0] != "&" and word[-1]!="…" and "http" not in word:
                        # print(word[-1]=="…")
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
        quote = get_grammatical_quote_from_input_array(words_from_tweets)
    else:
        quote = "nope"


    # api = TwitterAPI(os.environ.get("TWITTER_API_KEY"),
    #                  os.environ.get("TWITTER_API_SECRET"),
    #                  os.environ.get("TWITTER_ACCESS_TOKEN_KEY"),
    #                  os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"))
    #
    # r = api.request('application/rate_limit_status')
    #
    # # Print HTTP status code (=200 when no errors).
    # print(r.status_code)

    # r = api.request('statuses/filter', {'track':'pizza'})
    # r = api.request('statuses/update', {'status': 'I need pizza!'})

    #
    # headers = {"oauth_consumer_key": os.environ.get("TWITTER_API_KEY"),
    # "oauth_token": os.environ.get("TWITTER_BEARER_TOKEN")}
    #
    # tweets = requests.get(url, headers=headers)
    #
    # r = api.request('statuses/update', {'status': 'I need pizza!'})
    # if r.status_code == 200:
    #     print('SUCCESS')
    # else:
    #     print('FAILURE')

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
    app.run(host = '0.0.0.0', port = 7000)
