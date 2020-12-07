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

# unused helper function.
def pick_random_from_array(array):
    rand_int = randint(0,len(array)-1)
    return array[rand_int]

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
    relative_path = "/".join(filepath[:-2])
    write_filepath = "./" + relative_path + '/' + "tokenized_" + write_filename
    with open(write_filepath, "w") as new_file:
        for token in tokenized_words_array:
            new_file.write(token + " ")

def check_chars(my_quote, max_chars):
    """
    """
    count = 0
    return True if len(my_quote) < max_chars else False

def stop_after_punc(my_quote, limit_token_num):
    """
    """
    punc = [";",".","!","?",",","\""]
    stop_punc = [".","!","?"]
    quote = []
    j = 0
    for i in range(len(my_quote)):
        if my_quote[i] in punc:
            if i > limit_token_num and my_quote[i] in stop_punc:
                break
            else:
                part = " ".join(my_quote[j:i])+my_quote[i]
                quote.append(part)
                if i + 1 < len(my_quote):
                    j = i + 1
                else:
                    j = i
    last_part = " ".join(my_quote[j:i])+my_quote[i]
    quote.append(last_part)
    return quote

def nOrderMarkov(n,my_quote,words):
    """
    """
    instances = {}
    if len(my_quote) >= n:
        target_sequence = my_quote[-n]
    else:
        target_sequence = my_quote
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

def get_quote(file):
    """ Assumes input file has been tokenized and tokens are separated by spaces.
    """
    words = arrayFileWords(file)
    # words = tokenize_punc(words)
    rand_int = randint(0,len(words)-len(words)//3)
    # intialize word to a random word in case an uppercase word cannot be found.
    word = words[rand_int]
    # Starting off with an uppercase word...
    for i in range(rand_int):
        for j in range(len(words[i])):
            if words[i][j].isupper() and j==0:
                word = words[i]
                break
            else:
                continue # only check the first letter of each word
    my_quote = [word]
    while check_chars(my_quote, 500):
        if ORDER:
            n = ORDER
        else:
            n = 100
        instances = nOrderMarkov(n, my_quote, words)
        if instances:
            next_word = pick_next_word(instances)
        else:
            next_word = pick_random_word(words)

        my_quote.append(next_word)
    else:
        my_quote = stop_after_punc(my_quote,20)
        my_quote = " ".join(my_quote)
        return my_quote

def get_grammatical_quote_from_input(input):
    """
    """
    count = 0
    while count < 30:
        try:
            words = input.split(" ")
            words = tokenize_punc(words)
            not_found_count = 0
            found_upper = False
            # not found count is unecessary *****
            while not found_upper and not_found_count < 30:
                rand_int = randint(0,len(input)-1)
                # intialize word to a random word in case an uppercase word cannot be found.
                word = words[rand_int]
                # Starting off with an uppercase word...
                i = rand_int
                while not found_upper and i < len(input):
                    for j in range(len(words[i])):
                        if words[i][j].isupper() and j == 0 : # fixed problem here *****
                            found_upper = True
                            word = words[i]
                            break
                        else:
                            continue # only check the first letter of each word
                    i+=1
                not_found_count+=1
            # print(not_found_count,word)
            my_quote = [word]
            char_max = min(150,len(input))
            while check_chars(my_quote, char_max):
                if ORDER:
                    n = ORDER
                else:
                    n = 100
                instances = nOrderMarkov(n, my_quote, words)
                if instances:
                    next_word = pick_next_word(instances)
                else:
                    next_word = pick_random_word(words)
                my_quote.append(next_word)
            else:
                my_quote = stop_after_punc(my_quote,70)
                my_quote = " ".join(my_quote)
                return my_quote
        except IndexError:
            count+=1
        # print(count)
    return None

def get_grammatical_quote_from_input_array(array):
    """
    """
    count = 0
    while count < 30:
        try:
            words = array
            words = tokenize_punc(words)
            not_found_count = 0
            found_upper = False
            # not found count is unecessary *****
            while not found_upper and not_found_count < 30:
                rand_int = randint(0,len(array)-1)
                # intialize word to a random word in case an uppercase word cannot be found.
                word = words[rand_int]
                # Starting off with an uppercase word...
                i = rand_int
                while not found_upper and i < len(array):
                    for j in range(len(words[i])):
                        if words[i][j].isupper() and j == 0 : # fixed problem here *****
                            found_upper = True
                            word = words[i]
                            break
                        else:
                            continue # only check the first letter of each word
                    i+=1
                not_found_count+=1
            # print(not_found_count,word)
            my_quote = [word]
            char_max = min(80,len(array))
            while check_chars(my_quote, char_max):
                if ORDER:
                    n = ORDER
                else:
                    n = 100
                instances = nOrderMarkov(n, my_quote, words)
                if instances:
                    next_word = pick_next_word(instances)
                else:
                    next_word = pick_random_word(words)
                my_quote.append(next_word)
            else:
                # my_quote = insert_periods(my_quote)
                my_quote = stop_after_punc(my_quote,20)
                my_quote = " ".join(my_quote)
                return my_quote
        except IndexError:
            count+=1
        # print(count)
    return None

def get_any_quote_from_input(input):
    """
    """
    words = input.split(" ")
    words = tokenize_punc(words)
    rand_int = randint(0,len(words)-1)
    # intialize word to a random word from the corpus.s
    word = words[rand_int]
    my_quote = [word]
    char_max = min(500,len(input))
    while check_chars(my_quote, char_max):
        if ORDER:
            n = ORDER
        else:
            n = 100
        instances = nOrderMarkov(n, my_quote, words)
        if instances:
            next_word = pick_next_word(instances)
        else:
            next_word = pick_random_word(words)
        my_quote.append(next_word)
    else:
        my_quote = " ".join(my_quote)
        return my_quote

def insert_periods(arr):
    """
        iterate through the input array of words
        check to see if a word starts with an uppercase letter
        check to see if that word is a common noun and not a pronoun by opening
            the dictionary and checking to see if the word is in the dict
        if it is a common noun, add a period before it.
    """
    return
    for i in range(1,len(arr)):
        if arr[i][0].isupper():
            if binsearch_dictionary(arr[i]):
                arr[i-1].append(".")

def binsearch_dictionary(word_to_lookup,lower=None,upper=None):
    """
        perform a binary search on a locally-stored file
            containing all of the words in the English language
        return True or False if the word_to_lookup is in the file.
    """
    return
    # if not lower:
    #     word_to_lookup = word_to_lookup.lower()
    #     # open local dict_word file
    #         # turn the entire file into an array of words?
    #     dictionary_words = []
    #     lower = 0
    #     upper = len(dictionary_words)-1
    #     mid = (upper - lower)//2 + lower
    #     char_index = 0
    # while lower < upper:
    #     # if there is a match, match until there isn't a match or return True
    #     while dictionary_words[mid][char_index] == word_to_lookup[char_index]:
    #         char_index+=1
    #         if char_index > len(word_to_lookup):
    #             return True
    #     if char_index != 0:
    #
    #     # if there isn't a match, reset the char_index to look at the first letter of the word.
    #     char_index = 0
    #     # check to see if the first letter of the word_to_lookup is comes before the current word in the dictionary
    #     if dictionary_words[mid][char_index] > word_to_lookup[char_index]:
    #         pass
    #     # check to see if the first letter of the word_to_lookup is comes after the current word in the dictionary
    #     elif dictionary_words[mid][char_index] < word_to_lookup[char_index]:
    #         pass
    #     # ??? the first letter of the word matches but it's not the right word...
    #     else:



if __name__ == '__main__':
    _, read_filepath = sys.argv
    write_tokenized_file(read_filepath)
