from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData


def move_zkn_id_to_id(zettel_raw_data: ZettelRawData) -> None:
    if zettel_raw_data.metadata.get("zkn-id", None) is not None:
        if zettel_raw_data.metadata.get("id", None) is None:
            zettel_raw_data.metadata["id"] = zettel_raw_data.metadata["zkn-id"]

        del zettel_raw_data.metadata["zkn-id"]
