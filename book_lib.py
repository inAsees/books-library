import pymongo
from flask import Flask, request

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["library"]


@app.route('/api/search_book', methods=['POST'])
def get_book():
    text = request.json
    books_obj = mydb["BOOKS"].find()
    res = []
    for book in books_obj:
        if text["name"] in book["book_name"]:
            res.append(book["book_name"])
    if len(res) == 0:
        return {"status": "No book found"}, 400
    return {"books": res}, 200


app.run(debug=True)
