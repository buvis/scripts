from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData


def remove_duplicate_tags(zettel_raw_data: ZettelRawData) -> None:
    if zettel_raw_data.metadata.get("tags", None) is not None:
        zettel_raw_data.metadata["tags"] = list(set(zettel_raw_data.metadata["tags"]))
