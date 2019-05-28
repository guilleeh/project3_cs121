from flask import Flask, request, jsonify
import tokenizer
import database
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('search')
    db = database.Database()
    result = db.find(query)
    result = [each['postings'] for each in result]
    json = jsonify(result)
    print(json)
    return json

    

