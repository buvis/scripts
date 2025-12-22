import click

from fctracker.commands import CommandBalance, CommandTransactions


@click.group(help="CLI tool to manage accounts in foreign currencies")
def cli():
    pass


@cli.command("balance")
def balance():
    """Print current balance of all accounts and currencies"""
    cmd = CommandBalance()
    cmd.execute()


@cli.command("transactions")
@click.option("-a",
              "--account",
              default="",
              help="Only print transactions for given account")
@click.option("-c",
              "--currency",
              default="",
              help="Only print transactions for given currency")
@click.option(
    "-m",
    "--month",
    default="",
    help="Only print transactions for given month [YYYY-MM]",
)
def transactions(account="", currency="", month=""):
    """Print transactions"""
    cmd = CommandTransactions(account, currency, month)
    cmd.execute()


if __name__ == "__main__":
    cli()
