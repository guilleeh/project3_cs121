import json
from tokenizer import Tokenizer
import time

if __name__ == "__main__":
    tokens = Tokenizer()
    tokens.read_data('./WEBPAGES_RAW/bookkeeping.json')
    start = time.time()
    tokens.find_files()
    tokens.compute_tf_idf_and_insert_db()
    end = time.time()
    time = end - start
    full_time = "Hours: " + str(time / 60 / 60) + ", Minutes:" + str(time / 60)
    print(tokens.database.total_documents())
    tokens.database.show_all()
    print(full_time)