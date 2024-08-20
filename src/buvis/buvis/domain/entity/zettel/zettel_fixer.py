from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData

from .fixers import (
    align_h1_to_title,
    fix_title_format,
    move_tag_to_tags,
    move_zkn_id_to_id,
    remove_duplicate_tags,
    set_default_date,
    set_default_id,
    set_default_processed,
    set_default_publish,
    set_default_tags,
    set_default_title,
    set_default_type,
    sort_tags,
)


class ZettelFixer:
    @staticmethod
    def set_missing_defaults(zettel_raw_data: ZettelRawData) -> None:
        if zettel_raw_data.metadata.get("date", None) is None:
            set_default_date(zettel_raw_data)

        if zettel_raw_data.metadata.get("id", None) is None:
            set_default_id(zettel_raw_data)

        if zettel_raw_data.metadata.get("title", None) is None:
            set_default_title(zettel_raw_data)

        if zettel_raw_data.metadata.get("type", None) is None:
            set_default_type(zettel_raw_data)

        if zettel_raw_data.metadata.get("tags", None) is None:
            set_default_tags(zettel_raw_data)

        if zettel_raw_data.metadata.get("publish", None) is None:
            set_default_publish(zettel_raw_data)

        if zettel_raw_data.metadata.get("processed", None) is None:
            set_default_processed(zettel_raw_data)

    @staticmethod
    def ensure_consistency(zettel_raw_data: ZettelRawData) -> None:
        move_zkn_id_to_id(zettel_raw_data)
        ZettelFixer.set_missing_defaults(zettel_raw_data)
        move_tag_to_tags(zettel_raw_data)
        remove_duplicate_tags(zettel_raw_data)
        sort_tags(zettel_raw_data)
        fix_title_format(zettel_raw_data)
        align_h1_to_title(zettel_raw_data)
