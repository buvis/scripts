from decimal import Decimal


class Transaction:

    def __init__(self, date, amount, currency, rate):
        self.date = date
        self.amount = Decimal(f"{amount}")
        self.currency = currency
        self.rate = Decimal(f"{rate}")
