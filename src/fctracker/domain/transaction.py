from decimal import Decimal
import datetime


class Transaction:

    def __init__(self, date, amount, currency, rate):
        if isinstance(date, datetime.date):
            self.date = date
        else:
            self.date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        self.amount = Decimal(f"{amount}")
        self.currency = currency
        self.rate = Decimal(f"{rate}")

    def is_in_month(self, month):
        """Check if transaction's date falls to given month [YYYY-MM]"""
        month = datetime.datetime.strptime(month, "%Y-%m")

        return self.date.year == month.year and self.date.month == month.month
