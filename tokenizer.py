import json
import nltk
from bs4 import BeautifulSoup
import lxml

class Tokenizer:
    def __init__ (self):
        self.data = ''
        #This is where we should store all the tokens for all the files. Maybe use DICTIONARY
        self.tokens = {}

    def read_data(self, file):
        '''
        reads data from a json file and saves it in self.data
        '''
        with open(file, 'r') as myfile:
            self.data = json.load(myfile)

    def find_files(self):
        '''
        will go through each file, and call get_tokens on each
        '''
        i=0
        for key, value in self.data.items():
            # print('./WEBPAGES_RAW/' + key)
            self.get_tokens('./WEBPAGES_RAW/' + key) #maybe not working
            if(i == 4):
                break
            i+=1
            
    def print_all_tokens(self):
        i = 0
        for key, value in self.tokens.items():
            print(value)
            i += 1
            if i == 5:
                break

    def get_tokens(self, file):
        '''
        This function should return word tokens for a given file
        '''
        #http://nltk.org
        #https://pythonspot.com/tokenizing-words-and-sentences-with-nltk/ -has info on stop words and stemming
        
        with open(file, 'r') as myfile:
            raw_text = BeautifulSoup(myfile, 'lxml').get_text()
        self.tokens[file] = nltk.word_tokenize(raw_text) #maybe we need to open the file
        # print(self.tokens[file])
        
        
        