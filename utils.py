from datetime import datetime, date
from typing import Optional, List, Dict

from pymongo.database import Database


class Utilities:
    def __init__(self):
        self._id = None
        self._issue_date = None

    @staticmethod
    def get_date_delta(issue_date, return_date) -> int:
        """
        Get the delta between two dates.
        """
        delta = return_date - issue_date
        return delta.days

    @staticmethod
    def get_valid_date_format(date_str: str) -> Optional[date]:
        """
        Check if the date is valid and returns valid date with datatype date.
        :param date_str: date in string format.
        :return: datatype date or None.
        """
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            yr, mon, day = map(int, date_str.split('-'))
            return datetime(yr, mon, day)
        except ValueError:
            return None

    @staticmethod
    def is_book_available(book_name: str, mydb: Database) -> bool:
        for book in mydb["BOOKS"].find():
            if book_name == book["book_name"]:
                return True

        return False

    def is_book_issued(self, book_name: str, person_name: str, return_date: date, mydb: Database) -> Optional[bool]:
        for doc in mydb["TRANSACTIONS"].find():
            if book_name == doc["book_name"] and person_name == doc["person_name"] and doc["return_date"] is None and \
                    doc["total_rent"] == 0:
                self._id = doc["_id"]
                self._issue_date = doc["issue_date"]
                if not self.is_date_valid(return_date, doc["issue_date"]):
                    return None
                return True
        return False

    @staticmethod
    def is_book_returned(book_name: str, person_name: str, mydb: Database) -> bool:
        res = []
        for doc in mydb["TRANSACTIONS"].find():
            if book_name == doc["book_name"] and person_name == doc["person_name"] and isinstance(doc["return_date"]
                    , datetime) and doc["total_rent"] > 0:
                res.append(doc)
        if res:
            return True
        return False

    def update_return_date_and_total_rent(self, return_date: date, rent_per_day: int, mydb: Database) -> int:
        total_rent = self._get_total_rent(return_date, self._issue_date, rent_per_day)
        mydb["TRANSACTIONS"].update_one({"_id": self._id},
                                        {"$set": {"return_date": return_date, "total_rent": total_rent}})

        return total_rent

    @staticmethod
    def is_book_in_transactions(book_name: str, mydb: Database) -> bool:
        for doc in mydb["TRANSACTIONS"].find():
            if book_name == doc["book_name"]:
                return True

    @staticmethod
    def get_persons_having_book(book_name: str, mydb: Database) -> int:
        res = []
        for doc in mydb["TRANSACTIONS"].find():
            if book_name == doc["book_name"] and doc["return_date"] is None and doc["total_rent"] == 0:
                res.append(doc["person_name"])
        return len(res)

    @staticmethod
    def get_persons_who_returned_book(book_name: str, mydb: Database) -> List[str]:
        res = []
        for doc in mydb["TRANSACTIONS"].find():
            if book_name == doc["book_name"] and isinstance(doc["return_date"], datetime) and doc["total_rent"] > 0:
                res.append(doc["person_name"])
        return res

    @staticmethod
    def get_total_rent_generated_by_book(book_name: str, mydb: Database) -> int:
        res = []
        for doc in mydb["TRANSACTIONS"].find():
            if book_name == doc["book_name"] and isinstance(doc["return_date"], datetime) and doc["total_rent"] > 0:
                res.append(doc["total_rent"])
        return sum(res)

    @staticmethod
    def get_books_issued_to_person(person_name: str, mydb: Database) -> List[str]:
        res = []
        for doc in mydb["TRANSACTIONS"].find():
            if person_name == doc["person_name"]:
                res.append(doc["book_name"])
        return res

    @staticmethod
    def get_books_issued_in_date_range(start_date: date, end_date: date, mydb: Database) -> List[Dict]:
        res = []
        for doc in mydb["TRANSACTIONS"].find():
            if isinstance(doc["issue_date"], datetime) and start_date <= doc["issue_date"] <= end_date:
                res.append({"book_name": doc["book_name"], "person_name": doc["person_name"]})
        return res

    @staticmethod
    def rent_per_day(book_name: str, mydb: Database) -> int:
        for data in mydb["BOOKS"].find():
            if book_name == data["book_name"]:
                return data["rent_per_day"]

    @staticmethod
    def is_date_valid(issue_date: date, return_date: date) -> bool:
        """
        Check if the return date is valid.
        :param return_date: return date in date format.
        :param issue_date: issue date in date format.
        :return: True or False.
        """
        return return_date > issue_date

    def _get_total_rent(self, return_date: date, issue_date: date, rent_per_day: int) -> int:
        """
        Get the total rent of the book.
        :param return_date:
        :param issue_date:
        :return:
        """
        delta = self.get_date_delta(issue_date, return_date)
        return rent_per_day * delta
