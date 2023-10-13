from decimal import Decimal


class QuantifiedItem:

    def __init__(self, quantity):
        self.quantity = Decimal(f"{quantity}")

    def __copy__(self):
        return type(self)(self.quantity)

    def __repr__(self):
        return f"{self.quantity}"
