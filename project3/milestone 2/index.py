import json
from tokenizer import Tokenizer
import time

if __name__ == "__main__":
    tokens = Tokenizer()
    tokens.read_data('./WEBPAGES_RAW/bookkeeping.json')
    start = time.time()
    tokens.find_files()
    tokens.find_single_file("39/373", "mondego.ics.uci.edu/datasets/maven-contents.txt")
    tokens.compute_tf_idf_and_insert_db()
    end = time.time()
    time = end - start
    full_time = "Hours: " + str(time / 60 / 60) + ", Minutes:" + str(time / 60)
    print("TOTAL TOKENS: ", tokens.database.total_documents())
    print(full_time)