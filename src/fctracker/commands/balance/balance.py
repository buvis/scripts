from buvis.adapters import console

from fctracker.adapters import TransactionsDirScanner, TransactionsReader
from fctracker.domain import Account

import datetime


class CommandBalance:
    def __init__(self) -> None:
        print(
            "Something terribly losafnadsfl kajdfl kajdsfl aksjdflkajsd flaksd jf lkasdjf lasdjfl ajsdf"
        )
        pass

    def execute(self):
        scanner = TransactionsDirScanner()

        for account_name, currencies in scanner.accounts.items():
            for currency in currencies:
                account = Account(account_name, currency)
                reader = TransactionsReader(account)
                reader.get_transactions()
                console.print(account)
