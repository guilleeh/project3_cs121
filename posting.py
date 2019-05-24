
class Posting:
    '''
    Class representing a posting.

    '''
    def __init__ (self, file):
        self.file = file
        self.frequency = 1
        self.occurence_indices = []
        '''
        Indices of occurance: The location where a word occurs in a document
        Ex: “Go Warriors Go”
        Go is located at index 0 and 2
        '''
        self.tfidf = 0
        self.length_of_doc = 0


    def get_file(self):
        return self.file

    def get_tfidf(self):
        return self.tfidf
    
    def get_frequency(self):
        return self.tfidf
        
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

    
    #dict: {word: [posting]}
    

