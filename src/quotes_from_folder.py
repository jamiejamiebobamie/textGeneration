from web_functions import get_quote
import sys
import glob

from random import randint

# command line python file for generating quotes in bulk from a folder of tokenized text.
if __name__ == '__main__':
    _, num_quotes = sys.argv

    files = []
    # append filenames in data folder to a set
    for md in glob.glob("../public/data/*.md"):
        filename_parts = md.split("_")
        author = filename_parts[1].split(".")[0]
        files.append((author,md))

    write_filepath = "./quotes_from_data.md"

    i = 0
    num_quotes = int(num_quotes)
    while i < num_quotes:
        rand_index = randint(0,len(files)-1)
        read_filepath = files[rand_index][1]
        author = files[rand_index][0]
        quote = get_quote(read_filepath)
        with open(write_filepath, "a") as new_or_old_file:
            new_or_old_file.write(author + "\n")
            new_or_old_file.write(quote + "\n")
        print(author, quote)
        i+=1
        print(str(i) + " of " + str(num_quotes))
