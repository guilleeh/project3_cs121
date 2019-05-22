
class Posting:
    def __init__ (self, file):
        self.file = file
        self.occurence = 1

    def return_file(self):
        return self.file
    
    def update_occurence(self):
        self.occurence += 1

    
    #dict: {word: {0/0:[posting]}}
    

