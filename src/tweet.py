from collections import deque, Counter
import sys
from random import randint
import heapq

# hyperparameters
ORDER = 100 # the order of the markov model.
EPSILON = 2 # the amount to floor divide the max_length. a higher number allows
            # more words to be accepted despite how few words back they match the
            # sequence


def arrayFileWords(file):
    """Opens a file, puts the words into an array,
    closes the file and returns the array of strings"""
    f = open(file, "r")
    array = f.read().split()
    f.close()
    return array

# IN PROGRESS...
def tokenize_punc(array):
    """opens an array of strings, cycles through each word and then each character
    of a word and replaces that word with an exact copy but without punctuation. returns the array."""
    punctuation = [";", ".","!","?"]
    for i in range(len(array)):
        j = len(array[i]) - 1
        while j >= 0 and array[i][j] in punctuation:
                j-=1
        if j != len(array[i]) - 1:
            punc = array[i][-(len(array[i]) - j)]
            word = array[i][:j]
            array[i] = newWord
            array.insert(i+1,char)

    return array

def check_chars(my_tweet):
    """ Checks to see if the number of characters
        of the tweet are less than 120.
    """
    count = 0
    for word in my_tweet:
        count+=len(word)
        if count > 120:
            return False
    return True

def nOrderMarkov(n,my_tweet,words):
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
    rand_int = randint(0,len(words)-1)
    return words[rand_int]

def get_tweet(file):
    """
    I've cleaned this up a lot, but it's still pretty opaque.
    Need to refactor again and maybe even change my implementation.
    """
    words = arrayFileWords(file)
    rand_int = randint(0,len(words)-3000)
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
            n = randint(7,50)
        instances = nOrderMarkov(n, my_tweet, words)
        if instances:
            next_word = pick_next_word(instances)
            my_tweet.append(next_word)
        else:
            next_word = pick_random_word(words)
            print(next_word)
            my_tweet.append(next_word)
    else:
        return " ".join(my_tweet)

if __name__ == '__main__':
    file = '../public/data/Grimm.md'
    print(get_tweet(file))
