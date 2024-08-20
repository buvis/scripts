from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData

from .formatters import ZettelFormatterMarkdown


class ZettelFormatter:
    @staticmethod
    def as_markdown(zettel_raw_data: "ZettelRawData") -> str:
        return ZettelFormatterMarkdown.format(zettel_raw_data)
