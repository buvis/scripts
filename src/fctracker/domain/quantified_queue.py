import queue
from decimal import Decimal
from .quantified_item import QuantifiedItem


class QuantifiedQueue:

    def __init__(self):
        self._queue = queue.Queue()

    def put(self, quantity: float, payload):
        self._queue.put(QuantifiedItem(Decimal(f"{quantity}"), payload))

    def put_first(self, quantity: float, payload):
        self._queue.queue.insert(
            0, QuantifiedItem(Decimal(f"{quantity}"), payload))

    def get(self, quantity: float):
        quantity_left = Decimal(f"{quantity}")
        popped = []

        while quantity_left > 0:
            if self._queue.empty() is False:
                item = self._queue.get()
            else:
                raise queue.Empty

            if item.quantity >= quantity_left:
                quantity_return = item.quantity - quantity_left

                if quantity_return > 0:
                    self.put_first(quantity_return, item.payload)
                popped.append((float(quantity_left), item.payload))
                quantity_left = 0
            else:
                popped.append((float(item.quantity), item.payload))
                quantity_left -= item.quantity

        return popped

    def empty(self):
        return self._queue.empty()

    def __repr__(self):
        repr_items = [
            f"({item.quantity}, {item.payload})" for item in self._queue.queue
        ]

        return f"[{", ".join(repr_items)}]"
