import queue
from copy import copy
from decimal import Decimal
from .quantified_item import QuantifiedItem


class QuantifiedQueue:

    def __init__(self):
        self._queue = queue.Queue()

    def put(self, item: QuantifiedItem):
        self._queue.put(item)

    def put_first(self, item: QuantifiedItem):
        self._queue.queue.insert(0, item)

    def get(self, quantity: float):
        quantity_left = Decimal(f"{quantity}")
        popped = []

        while quantity_left > 0:
            if self._queue.empty() is False:
                item = self._queue.get()
            else:
                raise queue.Empty

            if item._get_quantity() >= quantity_left:
                quantity_remainder = item._get_quantity() - quantity_left

                if quantity_remainder > 0:
                    item_remainder = copy(item)
                    item_remainder._set_quantity(quantity_remainder)
                    self.put_first(item_remainder)
                item_taken = copy(item)
                item_taken._set_quantity(quantity_left)
                popped.append(item_taken)
                quantity_left = 0
            else:
                popped.append(item)
                quantity_left -= item._get_quantity()

        return popped

    def empty(self):
        return self._queue.empty()

    def __repr__(self):
        repr_items = [f"{item}" for item in self._queue.queue]

        return f"[{", ".join(repr_items)}]"

    def __iter__(self):
        return iter(self._queue.queue)
