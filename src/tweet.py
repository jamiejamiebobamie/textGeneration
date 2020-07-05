from collections import deque
import sys
import random
from histogram import lowercaseArray, arrayFileWords, nOrderMarkov, wordBeforeAfter


def checkChars(myTweet):
    """ Checks to see how many characters there are in myTweet.
    If there are less than 140 chars, then it returns True.
    """
    return True if len(myTweet) < 141 else False

if __name__ == '__main__':

    file = sys.argv[1]
    word = sys.argv[2]
    n = sys.argv[3]

    # take in the corpus of the given author and turn corpus
    # into an array of words and lowercase all words
    words = lowercaseArray(arrayFileWords(file))

    myTweet = word
    while checkChars(myTweet):
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
        print(myTweet)
