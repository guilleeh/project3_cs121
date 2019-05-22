
class Posting:
    '''
    Class representing a posting.

    '''
    def __init__ (self, file):
        self.file = file
        self.frequency = 1

    def return_file(self):
        return self.file
    
    def update_occurence(self):
        self.frequency += 1

    
    #dict: {word: {0/0:[posting]}}
    

