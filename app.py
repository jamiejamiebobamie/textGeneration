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
    # file = 'public/data/ALL.md'
    # file = 'public/data/Angelou.md'
    # file = 'public/data/Grimm.md'
    # file = 'public/data/Woolf.md'
    # file = 'public/data/Lovecraft.md'
    file = 'public/data/Poe.md'
    # file = 'public/data/Rowling.md'

    _tweet = get_tweet(file)
    return render_template('index.html', title='Home', tweet=_tweet)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 3000)
