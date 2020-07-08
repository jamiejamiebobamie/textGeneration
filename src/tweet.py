from collections import deque
import sys
import random

def arrayFileWords(file):
    """Opens a file, puts the words into an array,
    closes the file and returns the array of strings"""
    f = open(file, "r")
    array = f.read().split()
    f.close()
    return array

# NEED: to conserve punctuation by tokenizing it,
# inserting a new token after the given word has been removed of the punc.
def strip_Punc(array):
    """opens an array of strings, cycles through each word and then each character
    of a word and replaces that word with an exact copy but without punctuation. returns the array."""
    punctuation = ["@" , "#" , "$" , ":", ";", "_", "*" , "}" , "[" , "{" , "]" , "," , ".", "!" , "?"] #took out single and double quotes from this array
    for i, word in enumerate(array):
        newWord = ""
        for char in word:
            if char not in punctuation:
                newWord += char
        array[i] = newWord
    return array

# just for testing.
def lowercaseArray(array):
    """takes in an array of strings, uses a list comprehension to lowercase each letter"""
    array = [x.lower() for x in array]
    return array

def wordBeforeAfter(n, target_word, words_array):
    """
    Takes in an array of strings and looks for instances of the word in the array.
    If an instance of the word is found, the program compiles an array of length n
    words that come before the target word. Returns an array of arrays of:

    (1) the next word that comes after the instance of the target_word.
    (2) the target_word,
    (3) an array of n words before the instance of the target_word
    """
    instances = []
    for i, word in enumerate(words_array):
        if word == target_word:
            j = i - 1 # the last index before the current one
            words_before_target = []
            while j > i - n and j >= 0:
                words_before_target.append(words_array[j])
                j -= 1
            word_after_target = words_array[i+1]
            instance = [word_after_target, target_word] + words_before_target
            instances.append(instance)
    return instances

def nOrderMarkov(instances):
    """
    Takes in an array of word "instances".
    Instances are arrays that contain:
    (1) the next word that comes after the instance of the target_word.
    (2) the target_word,
    (3) an array of n words before the instance of the target_word.
    Returns a histogram of keys to counts.
    Keys consist of tuples of (next_word, target_word, words_before_target)
    """
    myDict = {}
    for instance in instances:
        _key = tuple(instance)
        if _key not in myDict:
            myDict[_key] = 1
        else:
            myDict[_key] += 1
    keys = list(myDict.keys())
    counts = list(myDict.values())
    return keys, counts

def check_chars(myTweet):
    """ Checks to see how many characters there are in myTweet.
    If there are less than 140 chars, then it returns True.
    """
    return True if len(myTweet) < 141 else False

def get_tweet(file,n):
    """
    I've cleaned this up a lot, but it's still pretty opaque.
    Need to refactor again and maybe even change my implementation.
    """
    words = arrayFileWords(file)
    rand_int = random.randint(0,len(words)-3000)
    word = words[rand_int]

    # Starting off with an uppercase word...
    for i in range(rand_int):
        for c in words[i]:
            if c.isupper():
                word = words[i]
                break
    myTweet = word
    while check_chars(myTweet):
        instances = wordBeforeAfter(n, word, words)
        keys, counts = nOrderMarkov(instances)
        j = 0
        storeIndex = 0
        stored = deque()
        # Creates a queue of indices into keys.
        # Only appends to queue if count of that particular key is higher than
            # the current maximum count. Kind of a wonky way of doing it, but it
            # introduces variation.
        for i in range(len(counts)):
            if counts[i] > j and len(stored) < n:
                storeIndex = i
                stored.append(i)
            elif counts[i] > j and len(stored) > n:
                stored.popleft()
                stored.append(i)
            j = counts[i]
        rand_int = random.randint(0, len(stored)-1)
        rand_index_into_keys = stored[rand_int]
        # the first word of key in keys is the next_word after the target.
        next_word = keys[rand_index_into_keys][0]
        word = next_word
        myTweet += " "
        myTweet += word
    else:
        return myTweet

if __name__ == '__main__':
    file = sys.argv[1]
    word = sys.argv[2]
    n = sys.argv[3]
    print(get_tweet(file,word,n))
