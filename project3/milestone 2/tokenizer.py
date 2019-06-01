import json
import nltk
from bs4 import BeautifulSoup
import lxml
from posting import Posting
from collections import defaultdict
import math
import database
import enchant
import re
from urllib.parse import urlparse

class Tokenizer:

    def __init__ (self):
        self.data = ''
        #This is where we should store all the tokens for all the files. Maybe use DICTIONARY
        self.tokens = {}
        self.total_number_of_docs = 0
        self.tokens_dict = {}
        self.database = database.Database(False)

    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        """
        parsed = urlparse(url)

        #Filter out any repeating directories
        if re.match(r"^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", url):
            return False

        #Filter out any urls with calendar
        if re.match("^(calendar+)*(.+day|.+month|.+year|.+Date).*$", url):
            return False


        #Filter out any links that require you to log in
        if re.match("^(.+)(sectok+)(.+)*$", url):
            return False

        # Filter out any links that have sidebyside in them
        if re.match("^(.+)(sidebyside+)(.+)*$", url):
            return False


        try:
            return ".ics.uci.edu" in parsed.hostname \
                   and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv| " \
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

        except TypeError:
            print("TypeError for ", parsed)
            return False

    def cleanhtml(self, raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def is_number(self, n):
        try:
            float(n)   # Type-casting the string to `float`.
                    # If string is not a valid `float`, 
                    # it'll raise `ValueError` exception
        except ValueError:
            return False
        return True

    def is_ascii(self, token):
        return all(ord(c) < 128 for c in token)

    def read_data(self, file):
        '''
        reads data from a json file and saves it in self.data
        '''
        with open(file, 'r') as myfile:
            self.data = json.load(myfile)
        print(len(self.data.keys()))
        

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
        for path, url in self.data.items():
            if(self.is_valid("https://" + url)):
                if( path != "39/373"):
                    self.create_tokens('./WEBPAGES_RAW/', path, url) #maybe not working
                    self.total_number_of_docs += 1
                print("Total: ", self.total_number_of_docs, " URL: ", url)
            
    def find_single_file(self, path, url):
        if( path != "39/373"):
            self.create_tokens('./WEBPAGES_RAW/', path, url)
                
    def create_stemmed_word_count_dictionary(self, raw_tokens):
        '''
        Takes in raw text, returns defaultdict of stemmed words in text
        '''
        s = nltk.PorterStemmer() 
        words_counted = defaultdict(int)
        for word in raw_tokens:
            word = word.lower()
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

        #Get title
        try:
            title = self.cleanhtml(str(soup.find_all("title")[0]))
            print("PRINTING TITLE")
            print(title)
        except IndexError:
            title = ""

        raw_text = soup.get_text()

        raw_tokens = nltk.word_tokenize(raw_text) 
        print("Compute RAW TOKENS")

        filtered_tokens = self.remove_stop_words(raw_tokens)
        print("Compute filtered_tokens")

        #Stemming of all the tokens gathered        
        words_counter = self.create_stemmed_word_count_dictionary(filtered_tokens)
        print("Compute word_dict")
        for word, count in words_counter.items():
            if(self.is_ascii(word) and (not self.is_number(word))):
                if len(word) < 182 and len(word) > 2: #Can't have large strings for db keys
                    posting = Posting(path, url, title)
                    posting.set_frequency(count)
                    posting.set_length_of_doc(len(raw_tokens))
                    if word not in self.tokens.keys():
                        self.tokens[word] = [posting]
                    else:
                        self.tokens[word].append(posting)
        if path == "www.ics.uci.edu/faculty":
            print(words_counter)

    def compute_tf_idf_and_insert_db(self):
        '''
        Sets the tf_idf score for each document based on a word
        '''
        tf = 0
        idf = 0
        convert_key = {"$": ascii("$"), "." : ascii(".")}
        print("Computing TF-IDF")
        for key, value in self.tokens.items():
            if key == "$" or key == ".":
                key = convert_key[key]
            
            new_entry = {"_id": key}
            posting_list = []
            
            print("WORD", key)
            for posting in value:
                print("INSIDE POSTINGS")
                tf = posting.frequency / posting.get_length_of_doc()
                print("WORD: ", key, self.total_number_of_docs, "/", len(value))
                idf = 1 + math.log10(self.total_number_of_docs / len(value))
                posting.set_tfidf(tf * idf)
                print("WORD: ", key, posting.posting_to_dictionary())
                posting_list.append(posting.posting_to_dictionary())
            
            sorted_postings = sorted(posting_list, key = lambda i: i['tfidf'], reverse=True)
            new_entry["postings"] = sorted_postings
            self.database.insert(new_entry)    









        
        