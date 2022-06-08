from datetime import datetime
import bson.json_util as json_util
import pymongo
from flask import Flask, request
from utils import Utilities

app = Flask(__name__)

utils = Utilities()
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["library"]


@app.route('/api/search_book', methods=['POST'])
def get_book():
    data = request.json
    books = mydb["BOOKS"].find()
    res = []
    for book in books:
        if data["name"] in book["book_name"]:
            res.append(json_util.dumps(book))
    if len(res) == 0:
        return {"status": "No books found"}, 400
    elif res:
        return {"books": res}, 200
    else:
        return {"status": "Some ERROR occurred."}, 400


@app.route('/api/books_in_price_range', methods=['POST'])
def get_books_in_price_range():
    data = request.json
    books_obj = mydb["BOOKS"].find()
    res = []
    for book in books_obj:
        if data["min_price"] <= book["rent_per_day"] <= data["max_price"]:
            res.append(json_util.dumps(book))
    if len(res) == 0:
        return {"status": "No books found"}, 400
    elif res:
        return {"books": res}, 200
    else:
        return {"status": "Some ERROR occurred."}, 400


@app.route('/api/books_in_pr_range_name_and_category', methods=['POST'])
def get_books_in_price_range_name_and_category():
    data = request.json
    books_obj = mydb["BOOKS"].find()
    res = []
    for book in books_obj:
        if data["min_price"] <= book["rent_per_day"] <= data["max_price"] and data["name"] in book["book_name"] and \
                data["category"] in book["category"]:
            res.append(json_util.dumps(book))
    if len(res) == 0:
        return {"status": "No books found"}, 400
    elif res:
        return {"books": res}, 200
    else:
        return {"status": "Some ERROR occurred."}, 400


@app.route('/api/book_issue', methods=['POST'])
def book_issue():
    data = request.json
    person_name = data["person_name"]
    book_name = data["book_name"]
    issue_date = data["issue_date"]
    final_date = utils.get_valid_date(issue_date)
    if final_date is None:
        return {"status": "Invalid date format '{}'".format(issue_date)}, 400

    if utils.is_book_available(book_name, mydb):
        mydb["TRANSACTIONS"].insert_one({"person_name": person_name, "book_name": book_name, "issue_date": final_date})
        return {"status": "Book '{0}' issued successfully to '{1}' on '{2}'.".format(book_name, person_name,
                                                                                     issue_date)}, 200
    else:
        return {"status": "Book '{}' not found".format(book_name)}, 400

    try:
        yr, mon, day = map(int, issue_date.split('-'))
        issue_date = datetime(yr, mon, day)
    except ValueError:
        return {"status": "Invalid issue date '{}'".format(issue_date)}, 400

    mydb["TRANSACTIONS"].insert_one({"person": person, "book": book_name, "issue_date": issue_date})
    return {"status": "Book '{0}' issued successfully to '{1}' on '{2}'.".format(book_name, person, issue_date)}, 200


if __name__ == '__main__':
    app.run(debug=True)
