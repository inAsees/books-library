import bson.json_util as json_util
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
            res.append(json_util.dumps(book))
    if len(res) == 0:
        return {"status": "No books found"}, 400
    elif res:
        return {"books": res}, 200
    else:
        return {"status": "Some ERROR occurred."}, 400


@app.route('/api/books_in_price_range', methods=['POST'])
def get_books_in_price_range():
    text = request.json
    books_obj = mydb["BOOKS"].find()
    res = []
    for book in books_obj:
        if text["min_price"] <= book["rent_per_day"] <= text["max_price"]:
            res.append(json_util.dumps(book))
    if len(res) == 0:
        return {"status": "No books found"}, 400
    elif res:
        return {"books": res}, 200
    else:
        return {"status": "Some ERROR occurred."}, 400


@app.route('/api/books_in_pr_range_name_and_category', methods=['POST'])
def get_books_in_price_range_name_and_category():
    text = request.json
    books_obj = mydb["BOOKS"].find()
    res = []
    for book in books_obj:
        if text["min_price"] <= book["rent_per_day"] <= text["max_price"] and text["name"] in book["book_name"] and \
                text["category"] in book["category"]:
            res.append(json_util.dumps(book))
    if len(res) == 0:
        return {"status": "No books found"}, 400
    elif res:
        return {"books": res}, 200
    else:
        return {"status": "Some ERROR occurred."}, 400


if __name__ == '__main__':
    app.run(debug=True)
