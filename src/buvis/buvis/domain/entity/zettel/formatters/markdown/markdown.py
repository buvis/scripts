from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData

from .helpers import (
    format_metadata,
    format_references,
    format_sections,
)


class ZettelFormatterMarkdown:
    FIRST_KEYS: tuple = ("id", "title", "date", "type", "tags", "publish", "processed")

    @staticmethod
    def format(zettel_raw_data: ZettelRawData) -> str:
        metadata_str = format_metadata(
            zettel_raw_data.metadata,
            ZettelFormatterMarkdown.FIRST_KEYS,
        )
        reference_str = format_references(zettel_raw_data.reference)
        sections_str = format_sections(zettel_raw_data.sections)

        return (
            f"---\n{metadata_str}\n---\n{sections_str}\n\n---\n{reference_str}"
        ).rstrip()
