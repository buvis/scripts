from buvis.domain.entity.zettel.zettel_data import ZettelData


def set_default_publish(zettel_data: ZettelData) -> None:
    zettel_data.metadata["publish"] = False
