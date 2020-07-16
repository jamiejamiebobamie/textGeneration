from web_functions import get_quote
import sys

# command line file for generating quotes in bulk.
if __name__ == '__main__':
    _, read_filepath, num_quotes = sys.argv

    filepath = read_filepath.split("/")
    write_filename = filepath[-1]
    relative_path = "/".join(filepath[:-1])
    write_filepath = "./quotes_"+write_filename

    i = 0
    num_quotes = int(num_quotes)
    while i < num_quotes:
        quote = get_quote(read_filepath)
        with open(write_filepath, "a") as new_or_old_file:
            new_or_old_file.write(quote + "\n")
        print(quote)
        print(str(i+1) + " of " + str(num_quotes))
        i+=1
