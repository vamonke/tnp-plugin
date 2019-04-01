import flask
from flask import request, jsonify
import pymongo
from bson.json_util import dumps
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["tnf"]
table = mydb["articles"]

@app.route('/', methods=['GET'])
def home():
    return '''<h1>The New Focus</h1>
    <p>A prototype API for The New Focus.</p>
    <h3>APIs</h3>
    <ul>
        <li>
            <a href="http://127.0.0.1:5000/api/breaking">/api/breaking</a>
        </li>
        <li>
            <a href="http://127.0.0.1:5000/api/trending">/api/trending</a>
        </li>
        <li>
            <a href="http://127.0.0.1:5000/api/catchup">/api/catchup</a>
        </li>
        <li>
            <a href="http://127.0.0.1:5000/api/lunchmunch">/api/lunchmunch</a>
        </li>
        <li>
            <a href="http://127.0.0.1:5000/api/sgfocus">/api/sgfocus</a>
        </li> 
        <li>
            <a href="http://127.0.0.1:5000/api/entertainment">/api/entertainment</a>
        </li>
    </ul>
'''


@app.route('/api/breaking', methods=['GET'])
def api_breaking():
    result = []
    query = { 'breaking': True }
    for x in table.find(query, {'_id': False }).limit(6):
        x['published_date'] = x['published_date'].strftime("%d %B %Y")
        result.append(x)
    return flask.jsonify(result)
    # return dumps({'stories': result})


@app.route('/api/trending', methods=['GET'])
def api_trending():
    result = []
    for x in table.find({}, {'_id': False }).limit(6).sort('fb_engagements', pymongo.DESCENDING):
        x['published_date'] = x['published_date'].strftime("%d %B %Y")
        result.append(x)
    return flask.jsonify(result)


@app.route('/api/catchup', methods=['GET'])
def api_catchup():
    result = []
    for x in table.find({}, {'_id': False }).limit(6):
        result.append(x)
    return flask.jsonify(result)


@app.route('/api/lunchmunch', methods=['GET'])
def api_lunchmunch():
    result = []
    query = { 'tag': 'FOOD & DRINK' }
    for x in table.find(query, {'_id': False }).limit(6).sort('published_date', pymongo.DESCENDING):
        x['published_date'] = x['published_date'].strftime("%d %B %Y")
        result.append(x)
    return flask.jsonify(result)


@app.route('/api/sgfocus', methods=['GET'])
def api_sgfocus():
    result = []
    query = { 'category': 'Singapore' }
    for x in table.find(query, {'_id': False }).limit(6).sort('published_date', pymongo.DESCENDING):
        x['published_date'] = x['published_date'].strftime("%d %B %Y")
        result.append(x)
    return flask.jsonify(result)


@app.route('/api/entertainment', methods=['GET'])
def api_entertainment():
    result = []
    query = {
        "$or": [
            { "category": "Movies" },
            { "category": "Music" },
            { "category": "TV" },
            { "category": "Star Style" },
            { "category": "School of Frock" }
        ]
    }
    for x in table.find(query, {'_id': False }).limit(6):
        x['published_date'] = x['published_date'].strftime("%d %B %Y")
        result.append(x)
    return flask.jsonify(result)

# @app.route('/api/v1/resources/books', methods=['GET'])
# def api_id():
#     # Check if an ID was provided as part of the URL.
#     # If ID is provided, assign it to a variable.
#     # If no ID is provided, display an error in the browser.
#     if 'id' in request.args:
#         id = int(request.args['id'])
#     else:
#         return "Error: No id field provided. Please specify an id."

#     # Create an empty list for our results
#     results = []

#     # Loop through the data and match results that fit the requested ID.
#     # IDs are unique, but other fields might return many results
#     for book in books:
#         if book['id'] == id:
#             results.append(book)

#     # Use the jsonify function from Flask to convert our list of
#     # Python dictionaries to the JSON format.
#     return jsonify(results)

app.run(host='0.0.0.0')