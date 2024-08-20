from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData


def sort_tags(zettel_raw_data: ZettelRawData) -> None:
    if zettel_raw_data.metadata.get("tags", None) is not None:
        zettel_raw_data.metadata["tags"] = sorted(zettel_raw_data.metadata["tags"])
