from flask import Flask, render_template
app = Flask(__name__)
from src.tweet import get_tweet

@app.route('/')
def _main():
    file = 'public/data/tokenized_Shakespeare.md'
    tweet = get_tweet(file)
    return render_template('index.html', title='Home',tweet=tweet)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)
