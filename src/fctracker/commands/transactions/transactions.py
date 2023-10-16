from buvis.adapters import console
from fctracker.domain import Account
from fctracker.adapters import TransactionsReader, TransactionsDirScanner


class CommandTransactions:

    def __init__(self, account="", currency="", month="") -> None:
        self.account = account.capitalize()
        self.currency = currency.upper()
        self.month = month

    def execute(self):
        scanner = TransactionsDirScanner()

        for account_name, currencies in scanner.accounts.items():
            if self.account == "" or (self.account == account_name):
                for currency in currencies:
                    if self.currency == "" or (self.currency == currency):
                        account = Account(account_name, currency)
                        reader = TransactionsReader(account)
                        reader.get_transactions()
                        console.print(
                            f"{account.name}[{account.currency}] transactions:"
                        )
                        console.nl()

                        filtered_transactions = [
                            t for t in reversed(account.transactions)
                            if (self.month == ""
                                or t.is_in_month(self.month) is True)
                        ]

                        index = len(filtered_transactions)

                        for transaction in filtered_transactions:
                            console.print(f"{index}. {transaction}")
                            index -= 1

                        console.nl()
