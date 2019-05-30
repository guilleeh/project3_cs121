from flask import Flask, request, jsonify
import tokenizer
import database
from flask_cors import CORS
import nltk

app = Flask(__name__, static_url_path='/client')
CORS(app)

@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('search')
    db = database.Database(False)
    s = nltk.stem.snowball.EnglishStemmer()
    query = s.stem(query.lower())
    result = db.find(query)
    result = [each['postings'] for each in result]
    json = jsonify(result)
    print(json)
    return json

    

