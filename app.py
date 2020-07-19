import os
from flask import Flask, render_template, request
app = Flask(__name__)
from src.web_functions import get_quote, pick_random_from_array, get_quote_from_input
from pymongo import MongoClient
import src.Quote_document
from flask_cors import CORS, cross_origin
# public API, allow all requests *
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
from random import randrange

# MONGO_URL = os.getenv('MONGOLAB_URI', 'mongodb://localhost:27017/database')
# MONGO_URL = os.environ.get('MONGO_URL')
# if not MONGO_URL:
#     MONGO_URL = "mongodb://localhost:27017/rest";

# app.config['MONGO_URI'] = MONGO_URL
# client = PyMongo(app)
client = MongoClient()
# client = PyMongo(app)

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
    new_quote_document = Quote()
    new_quote_document.quote = quote
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
        quote = get_quote_from_input(data)
        return {"quote": quote}
    else:
        return {"quote": ""}

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 7000)
