from datetime import datetime
from decimal import Decimal
from fctracker.domain import Account


def test_get_balance():
    account = Account("EUR")
    now = datetime.now()
    account.deposit(now, 20, 24.4988)
    balance = account.get_balance_local()
    assert balance == Decimal("489.98")
