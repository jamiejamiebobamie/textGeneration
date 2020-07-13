from collections import deque, Counter
import sys
import os
from random import randint
import heapq

# hyperparameters
ORDER = 100 # the order of the markov model.

# unused helper function.
def pick_random_file(folder_path):
    files = os.listdir(folder_path)
    return path +"/"+ files[randint(0,len(files)-1)]

def arrayFileWords(file):
    """
    """
    f = open(file, "r")
    array = f.read().split()
    f.close()
    return array

def tokenize_punc(words):
    """
    """
    punctuation = [";",".","!","?",",","\""]
    i = 0
    store_punc = []
    while i < len(words):
        j = 0
        new_word = []
        # keep track of the index
        punc = [i]
        while j < len(words[i]):
            if words[i][j] in punctuation:
                punc.append(words[i][j])
            else:
                new_word.append(words[i][j])
            j+=1
        words[i] = "".join(new_word)
        store_punc.append(punc)
        i+=1
    new_words = []
    j = 0
    for i in range(len(words)):
        index_of_punc = store_punc[j][0]
        if i == index_of_punc:
            # append the original word and then append the stored punctuation
                # associated with that index.
            new_words.append(words[i])
            for k in range(1,len(store_punc[j])):
                new_words.append(store_punc[j][k])
            # increment the counter to look at the next punctuation
            j+=1
        else:
            new_words.append(words[i])
    return new_words

def write_tokenized_file(read_filepath):
    """
    """
    words_array = arrayFileWords(read_filepath)
    tokenized_words_array = tokenize_punc(words_array)

    filepath = read_filepath.split("/")
    write_filename = filepath[-1]
    relative_path = "/".join(filepath[:-1])
    write_filepath = "./"+relative_path+write_filename
    with open(write_filepath, "w") as new_file:
        for token in tokenized_words_array:
            new_file.write(token + " ")

def check_chars(my_tweet):
    """
    """
    count = 0
    return True if len(my_tweet) < 100 else False

def stop_after_punc(my_tweet):
    """
    """
    punc = [";",".","!","?",",","\""]
    stop_punc = [".","!","?"]
    tweet = []
    j = 0
    for i in range(len(my_tweet)):
        if my_tweet[i] in punc:
            if i > 20 and my_tweet[i] in stop_punc:
                break
            else:
                part = " ".join(my_tweet[j:i])+my_tweet[i]
                tweet.append(part)
                if i + 1 < len(my_tweet):
                    j = i + 1
                else:
                    j = i
    last_part = " ".join(my_tweet[j:i])+my_tweet[i]
    tweet.append(last_part)
    return tweet

def nOrderMarkov(n,my_tweet,words):
    """
    """
    instances = {}
    if len(my_tweet) >= n:
        target_sequence = my_tweet[-n]
    else:
        target_sequence = my_tweet
    max_length = 0
    for i in range(len(words) - 1):
        j = -1
        k = i
        while k >= 0 and k < len(words) and abs(j) <= len(target_sequence):
            if words[k] == target_sequence[j]:
                k-=1
                j-=1
            else:
                break
        match = j < -1
        if match:
            # j is a negative index counting from the back of the sequence.
            max_length = min(j,max_length)
            if j <= max_length:
                _key = words[i+1]
                inInstances = instances.get(_key,False)
                if inInstances:
                    instances[_key]+=1
                else:
                    instances[_key]=1
    # may be empty.
    return instances

def pick_next_word(histogram_instances):
    """
    """
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
    # words = tokenize_punc(words)
    rand_int = randint(0,len(words)-len(words)//3)
    # intialize word to a random word in case an uppercase word cannot be found.
    word = words[rand_int]
    # Starting off with an uppercase word...
    for i in range(rand_int):
        for c in words[i]:
            if c.isupper():
                word = words[i]
                break
            else:
                continue # only check the first letter of each word
    my_tweet = [word]
    while check_chars(my_tweet):
        if ORDER:
            n = ORDER
        else:
            n = 100
        instances = nOrderMarkov(n, my_tweet, words)
        if instances:
            next_word = pick_next_word(instances)
        else:
            next_word = pick_random_word(words)

        my_tweet.append(next_word)
    else:
        my_tweet = stop_after_punc(my_tweet)
        my_tweet = " ".join(my_tweet)
        return my_tweet

if __name__ == '__main__':
    _, read_filepath = sys.argv
    write_tokenized_file(read_filepath)
