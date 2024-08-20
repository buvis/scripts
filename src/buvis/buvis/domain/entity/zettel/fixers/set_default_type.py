from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData

DEFAULT_TYPE = "note"


def set_default_type(zettel_raw_data: ZettelRawData) -> None:
    zettel_raw_data.metadata["type"] = DEFAULT_TYPE
