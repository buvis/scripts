from buvis.domain.entity.zettel.zettel_data import ZettelData
from buvis.domain.entity.zettel.zettel_formatter import ZettelFormatter

from .helpers import (
    format_metadata,
    format_reference,
    format_sections,
)


class ZettelFormatterMarkdown(ZettelFormatter):
    FIRST_KEYS: tuple = ("id", "title", "date", "type", "tags", "publish", "processed")

    @staticmethod
    def format(zettel_data: ZettelData) -> str:
        metadata_str = format_metadata(
            zettel_data.metadata,
            ZettelFormatterMarkdown.FIRST_KEYS,
        )
        reference_str = format_reference(zettel_data.reference)
        sections_str = format_sections(zettel_data.sections)

        return (
            f"---\n{metadata_str}\n---\n{sections_str}\n\n---\n{reference_str}"
        ).rstrip()
