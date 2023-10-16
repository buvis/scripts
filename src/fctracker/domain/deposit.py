from decimal import Decimal
from .quantified_item import QuantifiedItem
from .transaction import Transaction
from fctracker.adapters.config.config import cfg


class Deposit(Transaction, QuantifiedItem):

    def __init__(self, date, amount, currency, rate):
        Transaction.__init__(self, date, Decimal(f"{amount}"), currency,
                             Decimal(f"{rate}"))
        self.currency_symbol = cfg.currency[currency]["symbol"]

    def _get_quantity(self):
        return self.amount

    def _set_quantity(self, value):
        self.amount = value

    def __copy__(self):
        return type(self)(self.date, self.amount, self.currency, self.rate)

    def __repr__(self):
        return f"{self.amount} {self.currency_symbol} per {self.rate} on {self.date}"
