from tweet import get_tweet
import sys

if __name__ == '__main__':
    _, read_filepath, num_tweets = sys.argv

    filepath = read_filepath.split("/")
    write_filename = filepath[-1]
    relative_path = "/".join(filepath[:-1])
    write_filepath = "./quotes_"+write_filename

    i = 0
    num_tweets = int(num_tweets)
    while i < num_tweets:
        quote = get_tweet(read_filepath)
        with open(write_filepath, "a") as new_or_old_file:
            new_or_old_file.write(quote + "\n")
        print(str(i+1) + " of " + str(num_tweets))
        i+=1
