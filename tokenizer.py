import json
import nltk
from bs4 import BeautifulSoup
import lxml
from posting import Posting

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
            self.create_tokens('./WEBPAGES_RAW/', key) #maybe not working
            if(i == 90):
                break
            i+=1
            
    def print_all_tokens(self):
        for k, v in self.tokens.items():    
            print(k)
            for k2, v2 in v.items():
                print(k2, v2.occurence)
                

    def create_tokens(self, root, path):
        '''
        This function should return word tokens for a given file
        '''
        #http://nltk.org
        #https://pythonspot.com/tokenizing-words-and-sentences-with-nltk/ -has info on stop words and stemming
        
        ps = nltk.PorterStemmer()

        with open(root+path, 'r') as myfile:
            soup = BeautifulSoup(myfile, 'lxml')
        
        # kill all script and style elements
        for script in soup(["script", "style"]): #Source: https://stackoverflow.com/questions/22799990/beatifulsoup4-get-text-still-has-javascript
            script.decompose() #rip it out

        raw_text = soup.get_text()

        raw_tokens = nltk.word_tokenize(raw_text) 
        
        #Stemming of all the tokens gathered
        for word in raw_tokens:
            posting = Posting(path)
            stemmed_word = ps.stem(word) 
            if word not in self.tokens.keys():
                self.tokens[stemmed_word] = { path: posting }
            else:
                try:
                    self.tokens[stemmed_word][path].update_occurence()
                except KeyError:
                    self.tokens[stemmed_word] = { path: posting }


        
        