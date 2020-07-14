from flask import Flask, render_template
app = Flask(__name__)
from src.tweet import get_tweet, pick_random_from_array

@app.route('/')
def _main():
    file = 'src/quotes_tokenized_Shakespeare.md'
    tweets = []
    with open(file, "r") as pregenerated_tweets:
        for line in pregenerated_tweets:
            tweets.append(line)
    tweet = pick_random_from_array(tweets)
    return render_template('index.html', title='Home',tweet=tweet)

# testing. will crud to db.
@app.route('/generate')
def generate():
    read_filepath =  "public/data/tokenized_Shakespeare.md"
    filepath = read_filepath.split("/")
    write_filename = filepath[-1]
    relative_path = "/".join(filepath[:-1])
    write_filepath = "./src/quotes_"+write_filename
    quote = get_tweet(read_filepath)
    with open(write_filepath, "a") as tweets:
        tweets.write(quote + "\n")
    return render_template('index.html', title='Home',tweet=quote)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)
