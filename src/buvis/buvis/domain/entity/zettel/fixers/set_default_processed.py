from buvis.domain.entity.zettel.zettel_data import ZettelData


def set_default_processed(zettel_data: ZettelData) -> None:
    zettel_data.metadata["processed"] = False
