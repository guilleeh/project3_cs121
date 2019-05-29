import json
import nltk
from bs4 import BeautifulSoup
import lxml
from posting import Posting
from collections import defaultdict
import math
import database
from search import main
from search.crawler import Crawler
from search.frontier import Frontier

class Tokenizer:

    def __init__ (self):
        self.data = ''
        #This is where we should store all the tokens for all the files. Maybe use DICTIONARY
        self.crawler = main.Crawl()
        self.tokens = {}
        self.total_number_of_docs = 0
        self.tokens_dict = {}
        self.database = database.Database(True)

    def is_ascii(self, token):
        return all(ord(c) < 128 for c in token)

    def read_data(self, file):
        '''
        reads data from a json file and saves it in self.data
        '''
        with open(file, 'r') as myfile:
            self.data = json.load(myfile)
        #invert the dictionary to use the urls from crawler as keys
        self.data = {v: k for k, v in self.data.items()}

    def print_all_tokens(self):
        for k, v in self.tokens.items(): 
            print(k)
            space = "\t"
            for posting in v:
                posting_dict = posting.posting_to_dictionary()
                print(space, posting_dict["url"], posting_dict["tfidf"], posting_dict["frequency"])
                space += space
    
    def print_number_of_tokens(self):
        print(self.total_number_of_docs)

    def find_files(self):
        '''
        will go through each file, and call get_tokens on each
        '''
        for url in self.crawler.crawler.downloaded_urls:
            path = self.data[url]
            # print('./WEBPAGES_RAW/' + key)
            self.create_tokens('./WEBPAGES_RAW/', path, url) #maybe not working
            self.total_number_of_docs += 1
            print("Total: ", self.total_number_of_docs)
            # if(self.total_number_of_docs == 1):
            #     break
            
    def find_single_file(self, file, url):
        self.create_tokens('./WEBPAGES_RAW/', file, url)
                
    def create_stemmed_word_count_dictionary(self, raw_tokens):
        '''
        Takes in raw text, returns defaultdict of stemmed words in text
        '''
        s = nltk.stem.snowball.EnglishStemmer()
        words_counted = defaultdict(int)
        for word in raw_tokens:
            stemmed_word = s.stem(word)
            words_counted[stemmed_word] += 1
        return words_counted

    def remove_stop_words(self, raw_tokens):
        return [word for word in raw_tokens if word not in nltk.corpus.stopwords.words('english')]

    def create_tokens(self, root, path, url):
        '''
        This function should return word tokens for a given file
        '''
        #http://nltk.org
        #https://pythonspot.com/tokenizing-words-and-sentences-with-nltk/ -has info on stop words and stemming

        with open(root+path, 'r') as myfile:
            soup = BeautifulSoup(myfile, 'lxml')
        
        # kill all script and style elements
        for script in soup(["script", "style"]): #Source: https://stackoverflow.com/questions/22799990/beatifulsoup4-get-text-still-has-javascript
            script.decompose() #rip it out

        raw_text = soup.get_text()

        raw_tokens = nltk.word_tokenize(raw_text) 

        filtered_tokens = self.remove_stop_words(raw_tokens)
        
        #Stemming of all the tokens gathered        
        words_counter = self.create_stemmed_word_count_dictionary(filtered_tokens)

        for word, count in words_counter.items():
            if(self.is_ascii(word)):
                if len(word) < 182: #Can't have large strings for db keys
                    posting = Posting(path, url)
                    posting.set_frequency(count)
                    posting.set_length_of_doc(len(raw_tokens))
                    # posting.set_occurrence_indices(self.get_word_indices(raw_tokens, word))
                    if word not in self.tokens.keys():
                        self.tokens[word] = [posting]
                    else:
                        self.tokens[word].append(posting)

    def compute_tf_idf_and_insert_db(self):
        '''
        Sets the tf_idf score for each document based on a word
        '''
        tf = 0
        idf = 0
        convert_key = {"$": ascii("$"), "." : ascii(".")}
        for key, value in self.tokens.items():
            if key == "$" or key == ".":
                key = convert_key[key]
            
            new_entry = {"_id": key}
            posting_list = []
            
            for posting in value:
                tf = posting.frequency / posting.get_length_of_doc()
                idf = math.log10(self.total_number_of_docs / len(value))
                posting.set_tfidf(tf * idf)
                posting_list.append(posting.posting_to_dictionary())
            
            sorted_postings = sorted(posting_list, key = lambda i: i['tfidf'], reverse=True)
            new_entry["postings"] = sorted_postings
            self.database.insert(new_entry)    









        
        