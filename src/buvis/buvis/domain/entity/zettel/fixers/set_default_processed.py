from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData


def set_default_processed(zettel_raw_data: ZettelRawData) -> None:
    zettel_raw_data.metadata["processed"] = False
