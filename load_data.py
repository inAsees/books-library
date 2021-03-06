import pymongo
from dotenv import load_dotenv
import os

def insert_sample_dataset():
    books = mydb["BOOKS"]
    book_names = ["In Search of Lost Time", "Ulysses", "Don Quixote", "The Great Gatsby", "Moby Dick", "Hamlet",
                  "The Odyssey", "The Iliad", "One Hundred Years of Solitude", "The Republic", "The Book of Job",
                  "The Book of Kahlil", "War and Peace ", "Madame Bovary", "The Divine Comedy",
                  "The Brothers Karamazov",
                  "Crime and Punishment", "The Metamorphosis", "The Brothers Grimm", "The Picture of Dorian Gray", ]
    categories = ["Action and adventure", "Alternate history", "Children's", "Classic", "Comic book", "Horror", "Crime",
                  "Fairytale", "Mystery", "Poetry", "Romance", "Science fiction", "Thriller", "Young adult", "Fantasy",
                  "Historical fiction", "Historical novel", "Historical romance", "Historical thriller", "Horror", ]
    rents_per_day = [10, 15, 15, 30, 5, 10, 12, 20, 5, 50, 40, 11, 35, 15, 20, 50, 80, 10, 70, 10]

    for name, category, rent in zip(book_names, categories, rents_per_day):
        books.insert_one({"book_name": name, "category": category, "rent_per_day": rent})


if __name__ == "__main__":
    load_dotenv()
    client = pymongo.MongoClient(
        f"mongodb+srv://gurasees_singh:{os.environ.get('password')}@mongo-heroku-cluster.yemgj.mongodb.net/?retryWrites=true&w=majority")
    mydb = client["library"]

    insert_sample_dataset()
