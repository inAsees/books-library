from datetime import datetime, date
from typing import Optional

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
            if book_name == doc["book_name"] and person_name == doc["person_name"]:
                self._id = doc["_id"]
                self._issue_date = doc["issue_date"]
                if not self._is_return_date_valid(return_date, doc["issue_date"]):
                    return None
                return True
        return False

    def update_return_date_and_total_rent(self, return_date: date, rent_per_day: int, mydb: Database) -> int:
        total_rent = self._get_total_rent(return_date, self._issue_date, rent_per_day)
        mydb["TRANSACTIONS"].update_one({"_id": self._id},
                                        {"$set": {"return_date": return_date, "total_rent": total_rent}})

        return total_rent

    @staticmethod
    def rent_per_day(book_name: str, mydb: Database) -> int:
        for data in mydb["BOOKS"].find():
            if book_name == data["book_name"]:
                return data["rent_per_day"]

    def _get_total_rent(self, return_date: date, issue_date: date, rent_per_day: int) -> int:
        """
        Get the total rent of the book.
        :param return_date:
        :param issue_date:
        :return:
        """
        delta = self.get_date_delta(issue_date, return_date)
        return rent_per_day * delta

    @staticmethod
    def _is_return_date_valid(return_date: date, issue_date: date) -> bool:
        """
        Check if the return date is valid.
        :param return_date: return date in date format.
        :param issue_date: issue date in date format.
        :return: True or False.
        """
        return return_date > issue_date
