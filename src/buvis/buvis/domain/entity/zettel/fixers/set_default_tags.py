from buvis.domain.entity.zettel.zettel_data import ZettelData


def set_default_tags(zettel_data: ZettelData) -> None:
    zettel_data.metadata["tags"] = []
