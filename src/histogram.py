"""takes in a text file, counts the frequency of words in the text
returns a dictionary of word:frequency, key:value pairs"""

import sys
import timeit


def arrayFileWords(file):
    """opens a file, puts the words into an array,
    closes the file and returns the array of strings"""
    f = open(file, "r")
    array = f.read().split()
    f.close()
    return array
    #there might be a way of opening/closing (compacting the code) into less lines

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
    #string method .punc()


def lowercaseArray(array):
    """takes in an array of strings, uses a list comprehension to lowercase each letter"""
    #uppercase = ["I", "\'I" , "\"I"]
    array = [x.lower() for x in array] # if x not in uppercase]
    return array


#DICTIONARY HISTOGRAM ---------
def countWordsDict(array):
    """takes in an array of words (strings) and sorts them into a dictionary
    with the frequency (the # of times) that the word appears in the text as it's value,
    and the word as the key."""
    myDict = {}
    for word in array:
        if word not in myDict:
            myDict[word] = 1
        else:
            myDict[word] += 1
    return myDict

def unique_wordsDict(histogram):
    """takes in a histogram and returns the number of unique keys in it"""
    return len(histogram.keys())

def frequencyDict(histogram, word):
    """takes in a histogram and a word and returns the value of the word if the
    key exists in the dictionary, otherwise returns 0 """
    word = word.lower()
    if word in histogram:
        return histogram[word]
    else:
        return str(0)
##^^^^^DICTIONARY HISTOGRAM^^^^^




#List of lists HISTOGRAM ---------
def countWordsArray(array):
    """takes in an array of words (strings) and sorts them alphabetically
    cycles through the array and counts the entries in order,
   appending an array of the word and the word's frequency to array 'A'."""
    array.sort()
    A = []
    count = 0
    index = None
    for word in array:
        if word == index:
            count += 1
        else:
            A.append([index, count])
            index = word
            count = 1
    else:
        A.append([index, count])
        A.pop(0)
    return A

def unique_wordsArray(histogram):
    """takes in a histogram and returns the number of unique items in the array"""
    return len(histogram)

def frequencyArray(histogram, word):
    """takes in a histogram and a word and returns the # of times the word appears,
    according to second entry in the entry's array"""
    word = word.lower()
    for entry in histogram:
        if entry[0] == word:
            return entry[1]
    else:
        return "Your word is not in the text."
#^^^^^list of lists HISTOGRAM^^^^^




#List of tuples HISTOGRAM ---------
def countWordsTuples(array):
    """takes in an array of words (strings) and sorts them into an array of tuples
    with the word as the first entry in the tuple and frequency the second entry in the tuple."""
    array.sort()
    A = []
    count = 0
    index = None
    for word in array:
        if word == index:
            count += 1
        else:
            A.append((index, count)) #adding the entries in the array before going to the next word
            index = word
            count = 1
    else:
        A.append((index, count)) #adding the last entry in the array
        A.pop(0) #removing the instantiated index, this might be bad for performance "O(n)"
    return A

def unique_wordsTuples(histogram):
    """takes in a histogram and returns the number of unique keys in it"""
    return len(histogram)

def frequencyTuples(histogram, word):
    """takes in a histogram and a word and returns the value of the word if the
    words exists in the histogram, otherwise returns an error message """
    word = word.lower()
    for entry in histogram:
        if entry[0] == word:
            return entry[1]
    else:
        return "Your word is not in the text."
#^^^^^list of tuples HISTOGRAM^^^^^


def keysAsValues(histogram):
    """
    THIS FUNCTION BREAKS UP THE FUNCTIONALITY OF 'weightedWord'
    AND FOCUSES JUST ON CREATING A DICTIONARY
    ORGANZIED AROUND FREQENCY AS KEYS AND AN ARRAY OF WORDS AS VALUES

    takes in a dictionary histogram. splits the dictionary into two arrays,
    one of keys and the other: values.
    instantiates an empty dictionary called 'myDict'
    cycles through the array of values
    if the value is not in myDict adds the value to the dictionary
    and the key as the first element of an array, for example:

    myDict[1] = ["Boy"]

    this is a bit confusing, because I'm using the values from one dictionary
    and putting them into another dictionary as the keys, as well as turning the keys
    of one dictionary into elements of an array that make up the values in a new dictionary.

    for each time a new dictionary key is entered (which comes from the valueshistogram array)
    the value is checked against the highest_freq, and sets the highest_freq to the value

    """
    myDict = {}
    histogramKeys = list(histogram.keys())
    histogramValues = list(histogram.values())
    highest_freq = 0
    for i, value in enumerate(histogramValues):
        if value not in myDict:
            myDict[value] = [histogramKeys[i]]
            if value > highest_freq:
                highest_freq = value
        else:
            myDict[value].append(histogramKeys[i])
    return (myDict, highest_freq)


if __name__ == '__main__':
    file = str(sys.argv[1])
    print(countWordsArray(lowercaseArray(strip_Punc(arrayFileWords(file)))))
    #print(timeit.timeit(number = 10000))
