from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from buvis_scripts.core.domain.entity.zettel.zettel_data import ZettelData


class ZettelFormatter(ABC):
    @staticmethod
    @abstractmethod
    def format(zettel_data: "ZettelData") -> str:
        pass