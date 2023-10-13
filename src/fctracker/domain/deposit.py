from decimal import Decimal
from .quantified_item import QuantifiedItem
from .transaction import Transaction


class Deposit(Transaction, QuantifiedItem):

    def __init__(self, date, amount, currency, rate):
        Transaction.__init__(self, date, amount, currency, rate)
        QuantifiedItem.__init__(self, amount)

    @property
    def amount(self):
        return self.quantity

    @amount.setter
    def amount(self, value):
        self.quantity = Decimal(f"{value}")
        self._amount = Decimal(f"{value}")

    def __copy__(self):
        return type(self)(self.date, self.amount, self.currency, self.rate)

    def __repr__(self):
        return f"{self.amount} {self.currency} per {self.rate} on {self.date}"
