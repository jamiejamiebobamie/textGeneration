from flask import Flask, render_template
app = Flask(__name__)
from src.web_functions import get_quote, pick_random_from_array
from pymongo import MongoClient
from random import randrange

# pull quote from db.
@app.route('/')
def _main():
    db = client.database
    quotes_collection = db.quotes
    count = quotes_collection.count()
    quote = quotes_collection.find()[randrange(count)]["quote"]
    return render_template('index.html', title='Home',quote=quote)

# add quote to db.
@app.route('/generate')
def generate():
    db = client.database
    quotes_collection = db.quotes
    quote_document = {"quote":quote}
    quotes_collection.insert_one(quote_document)
    return render_template('index.html', title='Home',quote=quote)

# pull quote from file route.
@app.route('/pregenerated')
def pregenerated():
    file = 'src/quotes_tokenized_Shakespeare.md'
    quotes = []
    with open(file, "r") as pregenerated_quotes:
        for line in pregenerated_quotes:
            quotes.append(line)
    quote = pick_random_from_array(quotes)
    return render_template('index.html', title='Home',quote=quote)

# pull quote from db and serve as JSON.
    # should I password protect this?
@app.route('/api/v1/getQuote')
def serve_quote():
    db = client.database
    quotes_collection = db.quotes
    count = quotes_collection.count()
    quote = quotes_collection.find()[randrange(count)]
    return {"quote": quote["quote"]}

# add route for users to add text to the
    # "./public/data/quotes_tokenized_Shakespeare.md" file.
    # need CORS with password protection.

if __name__ == '__main__':
    client = MongoClient()
    app.run(host = '0.0.0.0', port = 3000)
