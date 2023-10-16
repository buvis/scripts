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
        return f"Added {self.amount} {self.currency_symbol} per {self.rate:.{cfg.local_currency['precision'] *2}f} {cfg.local_currency['symbol']}/{self.currency_symbol} (total {self.get_local_cost()} {cfg.local_currency['symbol']}) on {self.date.strftime('%Y-%m-%d')}"

    def get_local_cost(self):
        return Decimal(
            f"{(self.amount * self.rate):.{cfg.local_currency['precision']}f}")
