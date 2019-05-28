import json
from tokenizer import Tokenizer
import time

if __name__ == "__main__":
    tokens = Tokenizer()
    tokens.read_data('./WEBPAGES_RAW/bookkeeping.json')
    start = time.time()
    tokens.find_files()
    tokens.compute_tf_idf()
    end = time.time()
    time = end - start
    # tokens.print_all_tokens()
    tokens.get_tokens_and_postings_dict()
    full_time = "Hours: " + str(time / 60 / 60) + ", Minutes:" + str(time / 60)
    print(full_time)
    # tokens.database.show_all()