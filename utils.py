from datetime import datetime, date
from typing import Optional
from pymongo.database import Database


class Utilities:
    @staticmethod
    def get_date_delta(date1, date2):
        """
        Get the delta between two dates.
        """
        delta = date2 - date1
        return delta.days

    @staticmethod
    def get_valid_date(date_str: str) -> Optional[date]:
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
