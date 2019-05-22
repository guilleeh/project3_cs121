
class Posting:
    '''
    Class representing a posting.

    '''
    def __init__ (self, file):
        self.file = file
        self.frequency = 1
        self.occurence_indices = []
        #indices of occurance?
        self.tfidf = 0


    def return_file(self):
        return self.file

    def return_tfidf(self):
        return self.tfidf
    
    def return_frequency(self):
        return self.tfidf
    
    def increase_frequency(self):
        self.frequency += 1

    def set_frequency(self, count):
        self.frequency = count

    
    #dict: {word: [posting]}
    

