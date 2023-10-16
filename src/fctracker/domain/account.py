from decimal import Decimal
from fctracker.domain.quantified_queue import QuantifiedQueue
from fctracker.domain.deposit import Deposit
from fctracker.domain.withdrawal import Withdrawal
from fctracker.adapters.config.config import cfg


class Account:

    def __init__(self, name, currency):
        self.name = name
        self.currency = currency
        self._store = QuantifiedQueue()
        self.transactions = []

    def deposit(self, date, amount, rate):
        deposit_transaction = Deposit(date, amount, self.currency, rate)
        self._store.put(deposit_transaction)
        self.transactions.append(deposit_transaction)

    def withdraw(self, date, amount, description):
        withdrawn_deposits = self._store.get(amount)
        local_cost = Decimal("0")

        for wd in withdrawn_deposits:
            local_cost += wd.amount * wd.rate

        rate = local_cost / amount

        withdrawal_transaction = Withdrawal(date, amount, self.currency, rate,
                                            description)
        self.transactions.append(withdrawal_transaction)

        return withdrawal_transaction

    def get_balance(self):
        balance = Decimal("0")

        for deposit in self._store:
            balance += Decimal(f"{deposit.amount}")

        return Decimal(
            f"{balance:.{cfg.currency[self.currency]['precision']}f}")

    def get_balance_local(self):
        balance = Decimal("0")

        for deposit in self._store:
            balance += Decimal(f"{deposit.amount}") * Decimal(
                f"{deposit.rate}")

        return Decimal(f"{balance:.{cfg.local_currency['precision']}f}")

    def __repr__(self):
        return f"{self.name}[{self.currency}] balance: {self.get_balance()} {cfg.currency[self.currency]['symbol']} ({self.get_balance_local()} {cfg.local_currency['symbol']})"
