from flask import Flask, render_template
app = Flask(__name__)
import os
from random import randint
from src.tweet import get_tweet

def pick_random_file():
    path = 'public/data'
    mylist = os.listdir(path)
    return path +"/"+ mylist[randint(0,len(mylist))]

@app.route('/')
def _main():
    # file = pick_random_file()
    n = randint(7,15)
    file = 'public/data/ALL.md'
    _tweet = get_tweet(file,n)
    return render_template('index.html', title='Home', tweet=_tweet)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)
