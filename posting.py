
class Posting:
    '''
    Class representing a posting.

    '''
    def __init__ (self, file, url):
        self.file = file
        self.url = url
        self.frequency = 1
        self.occurence_indices = []
        '''
        Indices of occurance: The location where a word occurs in a document
        Ex: “Go Warriors Go”
        Go is located at index 0 and 2
        '''
        self.tfidf = 0 
        '''
        LOW TFIDF == WORD DOES NOT HAVE MUCH SIGNIFICANCE
        HIGH TFIDF == WORD IS MORE SIGNIFICANT SINCE ITS A RARE WORD
        '''
        self.length_of_doc = 0


    def get_file(self):
        return self.file

    def get_tfidf(self):
        return self.tfidf
    
    def get_frequency(self):
        return self.frequency
        
    def set_tfidf(self, tf_idf):
        self.tfidf = tf_idf
        
    def get_length_of_doc(self):
        return self.length_of_doc
    
    def increase_frequency(self):
        self.frequency += 1

    def set_frequency(self, count):
        self.frequency = count

    def set_length_of_doc(self, length):
        self.length_of_doc = length

    def set_occurrence_indices(self, list_of_indices):
        self.occurence_indices = list_of_indices

    def posting_to_dictionary(self):
        return {"file" : self.file, 
                "frequency": self.frequency, 
                "tfidf" : self.tfidf, 
                "total_words": self.length_of_doc, 
                "url": self.url}
    

