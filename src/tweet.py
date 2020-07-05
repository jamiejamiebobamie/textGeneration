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

def wordBeforeAfter(n, word, array):
    """takes in an array of strings,
    looks for instances of the word in the array.
    if an instance of the word is found,
    compiles an array of n words that come before the word.
    returns an array of tuples of
    (1) instance of word,
    (2) array of n words before the instance of the searched word, and
    (3) the next word that comes after the instance of the searched word."""
    instances = []
    for i, fileWord in enumerate(array):
        if fileWord == str.lower(str(word)):
            x = i -1
            beforeWords = []
            while x > (i - int(n)): #if you want n words after next-word
                beforeWords.append(array[x])
                x -= 1
            myTuple = (word, beforeWords, array[i+1])
            instances.append(myTuple)
    return instances

def nOrderMarkov(instances):
    """takes in an array of tuples (word, [array of n words before word], and next word),
    cycles through the array of tuples and appends the next word and the word to an array,
    and then appends the array of before words
    Does other stuff, see to-do at bottom to see output and how it's right, but also not..."""
    arrayofArrays = []
    myDict = {}
    for i, instance in enumerate(instances):
        myArray = [] #array in "backwards" chronological order from last word (next) to first word
        myArray.append(instance[2]) #next word
        myArray.append(instance[0]) #word
        myArray+=instance[1] #array of words before word
        arrayofArrays.append(myArray)
    for array in arrayofArrays:
        if tuple(array) not in myDict:
            myDict[tuple(array)] = 1
        else:
            myDict[tuple(array)] += 1
    keys = list(myDict.keys())
    values = list(myDict.values())
    return(keys, values)

def check_chars(myTweet):
    """ Checks to see how many characters there are in myTweet.
    If there are less than 140 chars, then it returns True.
    """
    return True if len(myTweet) < 141 else False

def get_tweet(file,word,n):
    # take in the corpus of the given author and turn corpus
    # into an array of words and lowercase all words
    words = lowercaseArray(arrayFileWords(file))
    # words = arrayFileWords(file)
    myTweet = word
    while check_chars(myTweet):
        keysValues = nOrderMarkov(wordBeforeAfter(n, word, words))
        x = 0
        storeIndex = 0
        stored = deque()
        for i, value in enumerate(keysValues[1]):
            if value > x and len(stored) < 7:
                x = value
                storeIndex = i
                stored.append(i)
            elif value > x and len(stored) > 7:
                x = value
                stored.popleft()
                stored.append(i)

        word = keysValues[0][stored[random.randint(0, len(stored)-1)]][0]
        myTweet += " "
        myTweet += word
    else:
        return myTweet

if __name__ == '__main__':
    file = sys.argv[1]
    word = sys.argv[2]
    n = sys.argv[3]
    print(get_tweet(file,word,n))
