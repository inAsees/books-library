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


@app.route('/api/books_in_per_range_name_and_category', methods=['POST'])
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
    final_date = utils.get_valid_date_format(issue_date)
    if final_date is None:
        return {"status": "Invalid date format '{}'".format(issue_date)}, 400

    if utils.is_book_available(book_name, mydb):
        mydb["TRANSACTIONS"].insert_one({"person_name": person_name, "book_name": book_name, "issue_date": final_date})
        return {"status": "Book '{0}' issued successfully to '{1}' on '{2}'.".format(book_name, person_name,
                                                                                     issue_date)}, 200
    else:
        return {"status": "Book '{}' not found".format(book_name)}, 400


@app.route('/api/book_return', methods=['POST'])
def book_return():
    data = request.json
    person_name = data["person_name"]
    book_name = data["book_name"]
    return_date = data["return_date"]

    final_date = utils.get_valid_date_format(return_date)
    if final_date is None:
        return {"status": "Invalid date format '{}'".format(return_date)}, 400

    check = utils.is_book_issued(book_name, person_name, final_date, mydb)
    if check is None:
        return {"status": "Invalid return date '{}'.".format(return_date)}, 400
    elif check:
        rent_per_day = utils.rent_per_day(book_name,mydb)
        total_rent = utils.update_return_date_and_total_rent(final_date, rent_per_day, mydb)
        return {"status": "Book '{0}' returned successfully by '{1}' on '{2}'. Total rent is Rs {3}".format(book_name,
                                                                                                            person_name,
                                                                                                            return_date,
                                                                                                            total_rent)}, 200
    else:
        return {"status": "Book '{}' not issued to '{}'.".format(book_name, person_name)}, 400


if __name__ == '__main__':
    app.run(debug=True)
