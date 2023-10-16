from decimal import Decimal
from .transaction import Transaction
from fctracker.adapters.config.config import cfg


class Withdrawal(Transaction):

    def __init__(self, date, amount, currency, rate, description):
        Transaction.__init__(self, date, amount, currency, rate)
        self.description = f"{description}"
        self.currency_symbol = cfg.currency[currency]["symbol"]

    def __copy__(self):
        return type(self)(self.date, self.amount, self.currency, self.rate)

    def __repr__(self):
        return f"{self.description} for {self.amount} {self.currency_symbol} per {self.rate} (total {self.get_local_cost()} {cfg.local_currency['symbol']}) on {self.date}"

    def get_local_cost(self):
        return Decimal(
            f"{(self.amount * self.rate):.{cfg.local_currency['precision']}f}")
