from abc import ABC, abstractmethod


class QuantifiedItem(ABC):

    @abstractmethod
    def __init__(self, quantity):
        pass

    @abstractmethod
    def _get_quantity(self):
        pass

    @abstractmethod
    def __copy__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass
