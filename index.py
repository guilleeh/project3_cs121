import json
from tokenizer import Tokenizer

if __name__ == "__main__":
    tokens = Tokenizer()
    tokens.read_data('./WEBPAGES_RAW/bookkeeping.json')
    tokens.find_files()
    tokens.print_all_tokens()
