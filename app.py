from flask import Flask
import pymongo
import tokenizer

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mydatabase"]
mycol = mydb["tokens"]
collist = mydb.list_collection_names()

if "tokens" in collist:
    print("DB Exists")

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"