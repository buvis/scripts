from buvis.adapters import console
from fctracker.domain import Account
from fctracker.adapters import TransactionsReader, TransactionsDirScanner


class CommandBalance:

    def __init__(self) -> None:
        pass

    def execute(self):
        scanner = TransactionsDirScanner()

        for account_name, currencies in scanner.accounts.items():
            for currency in currencies:
                account = Account(account_name, currency)
                reader = TransactionsReader(account)
                reader.get_transactions()
                console.print(account)
