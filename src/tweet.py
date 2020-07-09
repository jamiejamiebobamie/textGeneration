from collections import deque, Counter
import sys
from random import randint
import heapq

# hyperparameters
ORDER = 100 # the order of the markov model.
EPSILON = 2 # the amount to floor divide the max_length. a higher number allows
            # more words to be accepted despite how few words back they match the
            # sequence
NUM_TWEETS = 3


def arrayFileWords(file):
    """
    """
    f = open(file, "r")
    array = f.read().split()
    f.close()
    return array

# IN PROGRESS...
def tokenize_punc(words):
    """
    """
    punctuation = [";",".","!","?",",","\""]
    i = 0
    while i < len(words):
        j = 0
        new_word = []
        punc = []
        while j < len(words[i]):
            if words[i][j] in punctuation:
                punc.append(words[i][j])
            else:
                new_word.append(words[i][j])
            j+=1
        words[i] = "".join(new_word)
        # all punctuation is pulled from the word and placed as new tokens
            # after the word.
        j = 0
        while j < len(punc):
            i+=1
            words.insert(i,punc[j])
            j+=1
        i+=1
    return words

def check_chars(my_tweet):
    """
    """
    count = 0
    for word in my_tweet:
        count+=len(word)
        if count > 400:
            return False
    return True

def stop_after_punc(my_tweet):
    """
    """
    punc = [";",".","!","?",",","\""]
    stop_punc = [".","!","?"]
    _tweet = []
    j = 0
    for i in range(len(my_tweet)):
        if my_tweet[i] in punc:
            if i > 20 and my_tweet[i] in stop_punc:
                break
            else:
                part = " ".join(my_tweet[j:i])+my_tweet[i]
                _tweet.append(part)
                if i + 1 < len(my_tweet):
                    j = i + 1
                else:
                    j = i
    last_part = " ".join(my_tweet[j:i])+my_tweet[i]
    _tweet.append(last_part)
    return _tweet

def nOrderMarkov(n,my_tweet,words):
    """
    """
    instances = {}
    if len(my_tweet) >= n:
        target_sequence = my_tweet[-n]
    else:
        target_sequence = my_tweet
    max_length = 0
    for i in range(len(words)-1):
        j = -1
        k = i
        while k >= 0 and k < len(words) and abs(j) <= len(target_sequence):
            if words[k] == target_sequence[j]:
                k-=1
                j-=1
            else:
                break
        # if even one word matched...
        if j < -1:
            # j is negative so check which is lowest,
                # instead of using abs or j*-1
            max_length = min(j,max_length)
            if j <= max_length//EPSILON:
                _key = words[i+1]
                inInstances = instances.get(_key,False)
                if inInstances:
                    instances[_key]+=1
                else:
                    instances[_key]=1
    # !!! may be empty. let the exterior scope handle it.
    return instances

def pick_next_word(histogram_instances):
    """
    """
    # not the best time complexity...
    next_words = []
    most_frequent = heapq.nlargest(10,list(histogram_instances.values()))
    most_frequent = set(most_frequent)
    for word,count in histogram_instances.items():
        if count in most_frequent:
            next_words.append(word)
    rand_int = randint(0,len(next_words)-1)
    return next_words[rand_int]

def pick_random_word(words):
    """
    """
    rand_int = randint(0,len(words)-1)
    return words[rand_int]

def get_tweet(file):
    """
    """
    words = arrayFileWords(file)
    words = tokenize_punc(words)
    tweets = []
    # while len(tweets) < NUM_TWEETS:
    rand_int = randint(0,len(words)-len(words)//3)
    word = words[rand_int]
    # Starting off with an uppercase word...
    for i in range(rand_int):
        for c in words[i]:
            if c.isupper():
                word = words[i]
                break
    my_tweet = [word]
    while check_chars(my_tweet):
        if ORDER:
            n = ORDER
        else:
            n = 100
        instances = nOrderMarkov(n, my_tweet, words)
        if instances:
            next_word = pick_next_word(instances)
            my_tweet.append(next_word)
        else:
            next_word = pick_random_word(words)
            print(next_word)
            my_tweet.append(next_word)
    else:
        my_tweet = stop_after_punc(my_tweet)
        my_tweet = " ".join(my_tweet)
        return my_tweet
            # tweets.append(my_tweet)
    # return tweets

if __name__ == '__main__':
    file = '../public/data/Grimm.md'
    print(get_tweet(file))
