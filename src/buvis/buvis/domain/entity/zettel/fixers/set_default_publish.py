from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData


def set_default_publish(zettel_raw_data: ZettelRawData) -> None:
    zettel_raw_data.metadata["publish"] = False
