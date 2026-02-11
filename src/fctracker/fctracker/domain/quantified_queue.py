from __future__ import annotations

import queue
from collections.abc import Iterator
from copy import copy
from decimal import Decimal

from .quantified_item import QuantifiedItem


class QuantifiedQueue:
    def __init__(self) -> None:
        self._queue: queue.Queue[QuantifiedItem] = queue.Queue()

    def put(self, item: QuantifiedItem) -> None:
        self._queue.put(item)

    def put_first(self, item: QuantifiedItem) -> None:
        self._queue.queue.insert(0, item)

    def get(self, quantity: float) -> list[QuantifiedItem]:
        quantity_left = Decimal(f"{quantity}")
        popped = []

        while quantity_left > 0:
            if self._queue.empty() is False:
                item = self._queue.get()
            else:
                raise queue.Empty

            if item.get_quantity() >= quantity_left:
                quantity_remainder = item.get_quantity() - quantity_left

                if quantity_remainder > 0:
                    item_remainder = copy(item)
                    item_remainder.set_quantity(quantity_remainder)
                    self.put_first(item_remainder)
                item_taken = copy(item)
                item_taken.set_quantity(quantity_left)
                popped.append(item_taken)
                quantity_left = 0
            else:
                popped.append(item)
                quantity_left -= item.get_quantity()

        return popped

    def empty(self) -> bool:
        return self._queue.empty()

    def __repr__(self) -> str:
        repr_items = [f"{item}" for item in self._queue.queue]

        return f"[{', '.join(repr_items)}]"

    def __iter__(self) -> Iterator[QuantifiedItem]:
        return iter(self._queue.queue)
