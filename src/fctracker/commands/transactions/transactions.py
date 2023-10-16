from buvis.adapters import console
from fctracker.domain import Account, Deposit
from fctracker.adapters import TransactionsReader, TransactionsDirScanner, cfg
from rich.table import Table


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

                        filtered_transactions = [
                            t for t in reversed(account.transactions)
                            if (self.month == ""
                                or t.is_in_month(self.month) is True)
                        ]

                        table = Table(
                            show_header=True,
                            header_style="bold #268bd2",
                            show_lines=True,
                            title=f"{account}, transactions",
                        )
                        table.add_column("Seq.", style="italic #6c71c4")
                        table.add_column("Date", style="bold #839496")
                        table.add_column("Description")
                        table.add_column("Amount",
                                         justify="right",
                                         style="bold #2aa198")
                        table.add_column("Rate",
                                         justify="right",
                                         style="italic")
                        table.add_column("Outflow",
                                         justify="right",
                                         style="bold #dc322f")
                        table.add_column("Inflow",
                                         justify="right",
                                         style="bold #859900")

                        index = len(filtered_transactions)

                        for transaction in filtered_transactions:
                            if isinstance(transaction, Deposit):
                                description = "Deposit"
                                outflow = ""
                                inflow = f"{transaction.get_local_cost()} {cfg.local_currency['symbol']}"

                            else:
                                description = transaction.description
                                outflow = f"{transaction.get_local_cost()} {cfg.local_currency['symbol']}"
                                inflow = ""
                            table.add_row(
                                f"{index}",
                                transaction.date.strftime("%Y-%m-%d"),
                                description,
                                f"{transaction.amount} {transaction.currency_symbol}",
                                f"{transaction.rate:.{cfg.local_currency['precision'] *2}f} {cfg.local_currency['symbol']}/{transaction.currency_symbol}",
                                outflow,
                                inflow,
                            )
                            index -= 1
                        console.print(table)

                        console.nl()
