from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData


def set_default_tags(zettel_raw_data: ZettelRawData) -> None:
    zettel_raw_data.metadata["tags"] = []
