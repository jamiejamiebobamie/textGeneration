from flask import Flask, render_template
app = Flask(__name__)
from src.tweet import get_tweet, pick_random_from_array

@app.route('/')
def _main():
    # file = 'public/data/tokenized_Shakespeare.md'
    # tweet = get_tweet(file)
    file = 'src/quotes_tokenized_Shakespeare.md'
    tweets = []
    with open(file, "r") as pregenerated_tweets:
        for line in pregenerated_tweets:
            tweets.append(line)
    tweet = pick_random_from_array(tweets)

    return render_template('index.html', title='Home',tweet=tweet)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)
