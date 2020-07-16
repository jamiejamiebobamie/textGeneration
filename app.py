from flask import Flask, render_template
app = Flask(__name__)
from src.tweet import get_quote, pick_random_from_array
from pymongo import MongoClient
from random import randrange

@app.route('/')
def _main():
    db = client.database
    quotes_collection = db.quotes
    count = quotes_collection.count()
    quote = quotes_collection.find()[randrange(count)]["quote"]
    return render_template('index.html', title='Home',quote=quote)

@app.route('/generate')
def generate():
    db = client.database
    quotes_collection = db.quotes
    quote_document = {"quote":quote}
    quotes_collection.insert_one(quote_document)
    return render_template('index.html', title='Home',quote=quote)

@app.route('/pregenerated')
def pregenerated():
    file = 'src/quotes_tokenized_Shakespeare.md'
    quotes = []
    with open(file, "r") as pregenerated_quotes:
        for line in pregenerated_quotes:
            quotes.append(line)
    quote = pick_random_from_array(quotes)
    return render_template('index.html', title='Home',quote=quote)

# old route.
@app.route('/addToPregenerated')
def addToPregenerated():
    quote = "This a deperecated route. Go back to the homepage."
    return render_template('index.html', title='Home',quote=quote)

    # code used to add to the pregenerated quotes file.
    read_filepath =  "./public/data/tokenized_Shakespeare.md"
    filepath = read_filepath.split("/")
    write_filename = filepath[-1]
    relative_path = "/".join(filepath[:-1])
    write_filepath = "./src/quotes_"+write_filename
    quote = get_quote(read_filepath)
    with open(write_filepath, "a") as quotes:
        quotes.write(quote + "\n")
    return render_template('index.html', title='Home',quote=quote)

if __name__ == '__main__':
    client = MongoClient()
    app.run(host = '0.0.0.0', port = 3000)
