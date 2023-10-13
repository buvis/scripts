from decimal import Decimal
from fctracker.domain.quantified_queue import QuantifiedQueue
from fctracker.domain.deposit import Deposit


class Account:

    def __init__(self, currency):
        self.currency = currency
        self._store = QuantifiedQueue()

    def deposit(self, date, amount, rate):
        deposit_transaction = Deposit(date, amount, self.currency, rate)
        self._store.put(deposit_transaction)

    def get_balance_local(self):
        balance = Decimal("0")

        for deposit in self._store:
            balance += Decimal(f"{deposit.amount}") * Decimal(
                f"{deposit.rate}")

        return Decimal(f"{balance:.2f}")
