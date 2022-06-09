<!-- ABOUT THE PROJECT -->

## About The Project

This project mimics the work of a Librarian , who keeps all the records of the people to whom the  book is being
issued and the people who have returned the book.All the records are stored in a database(MongoDB).

### Built With

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com)
* [PyMongo](https://pymongo.readthedocs.io)
* [MongoDB](https://www.mongodb.com/)

### Prerequisites

<!-- This is an example of how to list things you need to use the software and how to install them. -->

* Python
* Flask
* PyMongo

## Getting Started

The Web Application is hosted by Heroku. You can access the application by only APIs , and you have to request for the
APIs using only 'POST' method.

### Following are the APIs that are available in the application,with their respective descriptions and Input/Output parameters.:

1. https://libofbooks.herokuapp.com/api/search_book :- This API is used to search for a book in the database. It takes
   the book name as the input and returns the details of the book.
   * Input: {'book_name' : 'Moby Dick'}
   * Output: {["books": "{\"_id\": {\"$oid\": \"62a206016585b0ad48dc496f\"}, \"book_name\": \"Moby Dick\", \"category\": \"Comic book\", \"rent_per_day\": 5}]} , status:200
     * If the book is not found in the database, it returns the status code as 400.
   
2. https://libofbooks.herokuapp.com/api/books_in_price_range :- This API is used to search for books in a price range. It takes two parameters.
   * Input: {'min_price' : '10', 'max_price' : '20'}
   * Output: {["books": "{\"_id\": {\"$oid\": \"62a206016585b0ad48dc496f\"}, \"book_name\": \"Moby Dick\", \"category\": \"Comic book\", \"rent_per_day\": 5}]} , status:200
     * If the book is not found in the database, it returns the status code as 400.
3. https://libofbooks.herokuapp.com/api/books_in_per_range_name_and_category :- This API is used to search for books in a price range , name and category. It takes four parameters.
   * Input: {'min_price' : '10', 'max_price' : '20', 'book_name' : 'Moby Dick', 'category' : 'Comic book'}
   * Output: {["books": "{\"_id\": {\"$oid\": \"62a206016585b0ad48dc496f\"}, \"book_name\": \"Moby Dick\", \"category\": \"Comic book\", \"rent_per_day\": 5}]} , status:200
     * If the book is not found in the database, it returns the status code as 400.
4. https://libofbooks.herokuapp.com/api/book_issue :- This API is used to issue a book to a user. It updates the data in the database.It takes three parameters.
   * Input: {"person_name":"kapil", "book_name":"Moby Dick", "issue_date":"2022-01-20"} , Date format: YYYY-MM-DD
   * Output: {"status": "Book 'Moby Dick' issued successfully to 'kapil' on '2022-01-20'."} , status:200
     * If there is any error in the Input parameters ,  it returns the status code as 400.
5. https://libofbooks.herokuapp.com/api/book_return :- This API is used to return a book to the library . It updates the data in the database after generating total rent.It takes three parameters.
   * Input: {"person_name":"kapil", "book_name":"Moby Dick", "return_date":"2022-01-20"} , Date format: YYYY-MM-DD
   * Output: {"status": "Book 'Moby Dick' returned successfully by 'kapil' on '2022-01-20'."} , status:200
     * If there is any error in the Input parameters ,  it returns the status code as 400.
6. https://libofbooks.herokuapp.com/api/search_books_issued_or_returned :- This API is used to search for books issued or returned by a user. It takes one parameter.
   * Input: {"book_name":"Moby Dick"}
   * Output: {"persons_having_book": 2, "persons_returned_book": ["chotu", "kapil"]} , status:200
     * If there is any error in the Input parameters ,  it returns the status code as 400.
7. https://libofbooks.herokuapp.com/api/total_rent_generated_by_book :- This API is used to search for total rent generated by a book. It takes one parameter.
   * Input: {"book_name":"Moby Dick"}
   * Output: {"total_rent": 10} , status:200
     * If there is any error in the Input parameters ,  it returns the status code as 400.
8. https://libofbooks.herokuapp.com/api/books_issued_to_person :- This API is used to search for books issued to a person. It takes one parameter.
   * Input: {"person_name":"kapil"}
   * Output: {"books": ["Moby Dick","Hamlet"]} , status:200
     * If there is any error in the Input parameters ,  it returns the status code as 400.
9. https://libofbooks.herokuapp.com/api/search_books_in_date_range :- This API is used to search for books in a date range. It takes two parameters.
   * Input: {"start_date":"2022-01-20", "end_date":"2022-01-26"} 
   * Output: {"books":[{"book_name":"Moby Dick","person_name":"chotu"},{"book_name":"Hamlet","person_name":"rohit"}]} , status:200
     * If there is any error in the Input parameters ,  it returns the status code as 400.



### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/inAsees/books_library.git
   ```
2. Install pip (package installer for Python)
   [here](https://pip.pypa.io/en/stable/installing/)
3. Install Python packages
   ```sh
   pip install requests
   pip install flask
   pip install pymongo
   ```

## Contact

Gurasees Singh - gurasees.singh121@gmail.com

Project Link: [https://github.com/inAsees/books_library](https://github.com/kevinclee26/mongo_heroku_demo)

