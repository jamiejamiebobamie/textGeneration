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

# pull quote from db.
@app.route('/')
def _main():
    db = client.database
    quotes_collection = db.quotes
    count = quotes_collection.count()
    quote = quotes_collection.find()[randrange(count)]["quote"]

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

# create quote from request.body and return as JSON.
@app.route('/api/v1/quote-from-url',methods=['POST'])
@cross_origin()
def serve_quote_from_url():
    url = request.get_json()
    print(url)
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

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 7000)
