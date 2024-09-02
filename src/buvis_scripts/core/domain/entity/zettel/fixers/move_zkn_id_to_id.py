from buvis_scripts.core.domain.entity.zettel.zettel_data import ZettelData


def move_zkn_id_to_id(zettel_data: ZettelData) -> None:
    if zettel_data.metadata.get("zkn-id", None) is not None:
        if zettel_data.metadata.get("id", None) is None:
            zettel_data.metadata["id"] = zettel_data.metadata["zkn-id"]

        del zettel_data.metadata["zkn-id"]
