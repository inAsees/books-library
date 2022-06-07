import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["library"]
books = mydb["BOOKS"]
book_name = ["In Search of Lost Time", " Ulysses ", "Don Quixote", "The Great Gatsby", "Moby Dick", "Hamlet",
             "The Odyssey", "The Iliad", "One Hundred Years of Solitude", "The Republic", "The Book of Job",
             "The Book of Kahlil", "War and Peace ", "Madame Bovary", "The Divine Comedy", "The Brothers Karamazov",
             "Crime and Punishment", "The Metamorphosis", "The Brothers Grimm", "The Picture of Dorian Gray", ]
category = ["Action and adventure", "Alternate history", "Children's", "Classic", "Comic book", "Horror", "Crime",
            "Fairytale", "Mystery", "Poetry", "Romance", "Science fiction", "Thriller", "Young adult", "Fantasy",
            "Historical fiction", "Historical novel", "Historical romance", "Historical thriller", "Horror", ]
rent_per_day = [10, 15, 15, 20, 5, 10, 12, 20, 5, 5, 8, 11, 14, 15, 20, 5, 8, 10, 10, 11]

for name, category, rent in zip(book_name, category, rent_per_day):
    books.insert_one({"book_name": name, "category": category, "rent_per_day": rent})
