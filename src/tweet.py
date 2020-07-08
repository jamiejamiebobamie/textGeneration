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
    words that come before the target word. Returns an array of tuples of:
    (1) the target_word,
    (2) an array of n words before the instance of the target_word, and
    (3) the next word that comes after the instance of the target_word.
    """
    instances = []
    for i, word in enumerate(words_array):
        if str.lower(word) == str.lower(target_word):
            j = i - 1 # the last index before the current one
            words_before_target = []
            while j > i - n and j >= 0:
                words_before_target.append(words_array[j])
                j -= 1
            word_after_target = words_array[i+1]
            instance = (target_word, words_before_target, word_after_target)
            instances.append(instance)
    return instances

def nOrderMarkov(instances):
    """
    Takes in an array of word "instances".
    Instances are tuples that contain:
    (1) the target_word,
    (2) an array of n words before the instance of the target_word, and
    (3) the next word that comes after the instance of the target_word.
    Cycles through the instances and appends the next word and the target_word
    to an array, and then appends the array of before words
    """
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

def get_tweet(file,n):
    # take in the corpus of the given author and turn corpus
    # into an array of words and lowercase all words
    # words = lowercaseArray(arrayFileWords(file))

    words = arrayFileWords(file)
    rand_int = random.randint(0,len(words)-1)
    word = words[rand_int]
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
