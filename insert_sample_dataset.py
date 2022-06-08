from datetime import datetime

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["library"]


def insert_sample_dataset():
    books = mydb["BOOKS"]
    book_names = ["In Search of Lost Time", " Ulysses ", "Don Quixote", "The Great Gatsby", "Moby Dick", "Hamlet",
                  "The Odyssey", "The Iliad", "One Hundred Years of Solitude", "The Republic", "The Book of Job",
                  "The Book of Kahlil", "War and Peace ", "Madame Bovary", "The Divine Comedy",
                  "The Brothers Karamazov",
                  "Crime and Punishment", "The Metamorphosis", "The Brothers Grimm", "The Picture of Dorian Gray", ]
    categories = ["Action and adventure", "Alternate history", "Children's", "Classic", "Comic book", "Horror", "Crime",
                  "Fairytale", "Mystery", "Poetry", "Romance", "Science fiction", "Thriller", "Young adult", "Fantasy",
                  "Historical fiction", "Historical novel", "Historical romance", "Historical thriller", "Horror", ]
    rents_per_day = [10, 15, 15, 30, 5, 10, 12, 20, 50, 5, 40, 11, 35, 15, 20, 5, 80, 10, 70, 10]

    for name, category, rent in zip(book_names, categories, rents_per_day):
        books.insert_one({"book_name": name, "category": category, "rent_per_day": rent})


def book_issue():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["library"]
    transactions = mydb["TRANSACTIONS"]
    persons = ["ram", "shyam", "geeta", "sidhu", "iyyer", "gopal", "ruby", "lalita", "sargun", "chotu"]
    books_name = ["In Search of Lost Time", " Ulysses ", "Don Quixote", "The Great Gatsby", "Moby Dick", "Hamlet",
                  "The Odyssey", "The Iliad", "One Hundred Years of Solitude", "The Republic", "The Book of Job",
                  "The Book of Kahlil", "War and Peace ", "Madame Bovary", "The Divine Comedy",
                  "The Brothers Karamazov", "Crime and Punishment", "The Metamorphosis", "The Brothers Grimm",
                  "The Picture of Dorian Gray"]
    issue_dates = ["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04", "2020-01-05", "2020-01-06", "2020-01-07",
                   "2020-01-08", "2020-01-09", "2020-01-10"]
    return_dates = ["2020-01-11", "2020-01-12", "2020-01-13", "2020-01-14", "2020-01-15", "2020-01-16", "2020-01-17",
                    "2020-01-18", "2020-01-19", "2020-01-20"]
    issue_date = None
    return_date = None
    for person, book, issue, return_date in zip(persons, books_name, issue_dates, return_dates):
        try:
            yr, mon, day = map(int, issue.split('-'))
            issue_date = datetime(yr, mon, day)
        except ValueError:
            print("Invalid issue date:", issue)

        try:
            yr, mon, day = map(int, return_date.split('-'))
            return_date = datetime(yr, mon, day)
        except ValueError:
            print("Invalid return date:", return_date)

        transactions.insert_one({"person": person, "book": book, "issue_date": issue_date, "return_date": return_date})


if __name__ == "__main__":
    insert_sample_dataset()
    book_issue()
