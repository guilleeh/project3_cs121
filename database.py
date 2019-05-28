import pymongo

class Database:
    '''
    Database class to perform CRUD operations on MONGODB DB
    '''
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["mydatabase"]

        if "tokens" in self.db.collection_names():
            self.db["tokens"].drop()

        self.collection = self.db["tokens"]


    def insert(self, token):
        response = self.collection.insert(token, check_keys=False)
        return response

    def show_all(self):
        for token in self.collection.find():
            print(token)

    def find(self, word):
        query = {"_id": word}
        result = self.collection.find(query)
        for each in result:
            print(each)

    


    
