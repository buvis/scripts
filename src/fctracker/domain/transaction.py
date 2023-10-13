from decimal import Decimal


class Transaction:

    def __init__(self, date, amount, currency, rate):
        self.date = date
        self._amount = amount
        self.currency = currency
        self.rate = Decimal(f"{rate}")
