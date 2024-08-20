from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData


def move_tag_to_tags(zettel_raw_data: ZettelRawData) -> None:
    if zettel_raw_data.metadata.get("tag", None) is not None:
        if zettel_raw_data.metadata.get("tags", None) is None:
            zettel_raw_data.metadata["tags"] = []

        if isinstance(zettel_raw_data.metadata["tag"], str):
            zettel_raw_data.metadata["tag"] = [zettel_raw_data.metadata["tag"]]

        zettel_raw_data.metadata["tags"].extend(zettel_raw_data.metadata["tag"])

        del zettel_raw_data.metadata["tag"]
