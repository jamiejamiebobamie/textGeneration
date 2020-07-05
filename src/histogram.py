import sys

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
    punctuation = ["@" , "#" , "$" , ":", ";", "_", "*" , "}" , "[" , "{" , "]" , "," , ".", "!" , "?"] #took out single and double quotes from this array
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

def wordBeforeAfter(n, word, array):
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
