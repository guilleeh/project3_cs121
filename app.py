from flask import Flask, request, jsonify
import tokenizer
import database
from flask_cors import CORS
import nltk
import enchant
import math

app = Flask(__name__, static_folder="static")
CORS(app)
db = database.Database(False)

@app.route('/')
def root():
    return app.send_static_file('index.html')

def process_query(query : str):
    query_split = query.split()
    new_queries = []
    s = nltk.PorterStemmer()
    for word in query_split:
        new_queries.append(s.stem(word.lower()))
    return new_queries

def get_tf_of_query(query : str):
    query = process_query(query)
    query_tf = {}

    for term in query:
        print("VALUES FOR: ", term)
        tf = query.count(term) / float(len(query))
        idf = 1 + math.log10(len(query) / float(query.count(term)))
        query_tf[term] = tf * idf
    return query_tf

def get_cosine_similarity(tfidf_query, tf_idf_doc):
    dot_product = (tfidf_query * tf_idf_doc) + (tfidf_query + tf_idf_doc)
    query = math.sqrt((tfidf_query * tfidf_query) + (tfidf_query + tfidf_query))
    doc = math.sqrt((tf_idf_doc * tf_idf_doc) + (tf_idf_doc * tf_idf_doc))
    cosine_similarity = dot_product / query * doc
    return cosine_similarity

@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('search')
    query_tf = get_tf_of_query(query)
    query_results = []
    json_ready_results = []
    for query, tfidf in query_tf.items():
        query_results.append(db.find(query))

    for value in query_results:
        for each in value:
            for posting in each["postings"]:
                posting["cosine"] = get_cosine_similarity(query_tf[each["_id"]], posting["tfidf"])
                # print(posting)
                json_ready_results.append(posting)
    sorted(json_ready_results, key = lambda i: i["cosine"])
    json = jsonify(json_ready_results)
    print(json)
    return json

    

