import sys
import string
import random

from collections import deque
import sys
import string
import random
from histogram import countWordsDict, countWordsArray, arrayFileWords, strip_Punc, lowercaseArray, keysAsValues


if __name__ == '__main__':
        file = str(sys.argv[1])
        word = sys.argv[2]
        n = sys.argv[3]

def arrayFileWords(file):
    """opens a file, puts the words into an array,
    closes the file and returns the array of strings"""
    f = open(file, "r")
    array = f.read().split()
    f.close()
    return array

def strip_Punc(array):
    """opens an array of strings, cycles through each word and then each character
    of a word and replaces that word with an exact copy but without punctuation. returns the array."""
    punctuation = ["!", "@" , "#" , "$" , "." , ",", "?", ":", ";", "-", "_", "*"]
    for i, word in enumerate(array):
        newWord = ""
        for char in word:
            if char not in punctuation:
                newWord += char
        array[i] = newWord
    return array

def lowercaseArray(array):
    """takes in an array of strings, uses a list comprehension to lowercase each letter"""
    array = [x.lower() for x in array]
    return array

def wordBeforeAfter(array):
    """takes in an array of strings,
    using the global variables word and n,
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
            #while x > (i - int(n) - 1): #if you want n words before word
            while x > (i - int(n)): #if you want n words after next-word
                beforeWords.append(array[x])
                x -= 1
            myTuple = (word, beforeWords, array[i+1])
            instances.append(myTuple)
    return instances

def firstOrderMarkov(arrayOfTuples):
    """takes in an array of tuples of (word, [array of words before word], next word that comes after word)
    creates a dictionary of {next word : number of instances}. splits the dictionary into a 'twin index' of two arrays: keys and values.

    "twin index" = keys[0] and values[0] reference the key and value pair of the dictionary that was 'split'.

    for each key the function prints to console what the likelihood is of that key appearing as the next word."""
    myDict = {}
    for i, instance in enumerate(arrayOfTuples):
        if instance[2] not in myDict:
            myDict[arrayOfTuples[i][2]] = 1
        else:
            myDict[arrayOfTuples[i][2]] += 1
    keys = list(myDict.keys())
    values = list(myDict.values())
    print(keys)
    print(values)

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

def checkChars(myTweet):
    """checks to see how many characters there are in myTweet. if there are less
    than 140 then it returns True."""
    counter = 0
    for chars in myTweet:
        counter += 1
    if counter < 141:
        return True
    else:
        return False

# word = random.randint(0, len(arrayFileWords(file))-1)
myTweet = str(word)
# upperRange = int(n)                          #creates variety
# lowerRange = (int(n) - (int(n)//1.3))        #consider changing
words = lowercaseArray(arrayFileWords(file))
# if lowerRange < 1:
#     lowerRange = 1
while checkChars(myTweet):
    keysValues = nOrderMarkov(wordBeforeAfter(words))
    x = 0
    storeIndex = 0
    stored = deque()#[]
    for i, value in enumerate(keysValues[1]):
        if value > x and len(stored) < 7:                         #right now it is just going to the highest frequency word, use herd_immunity virus_repro-style
            x = value
            storeIndex = i
            stored.append(i)
        elif value > x and len(stored) > 7:
            x = value
            stored.popleft()
            stored.append(i)
    # chosen = stored[random.randint(0, len(stored)-1)]
    # word = keysValues[0][random.randint(0, storeIndex)][0]
    word = keysValues[0][stored[random.randint(0, len(stored)-1)]][0]
    # word = keysValues[0][stored[chosen]][0]
    # print((word, len(stored)))
    # n = random.randint(lowerRange, upperRange)
    myTweet += " "
    # word = keysValues[0][storeIndex][0]       #i could check to see if the word is in the sentence, would completely get rid of repeats tho...
    # n = random.randint(lowerRange, upperRange)#i could check to see if the chars in the word match the up with the last 20 chars, if so use next most frequent word
    # myTweet += " "                            #maybe use a queue to do first in, first out of words or chars to consistently check; repetition of the same word is killing me
    myTweet += word
    checkChars(myTweet)
else:
    print(myTweet)
