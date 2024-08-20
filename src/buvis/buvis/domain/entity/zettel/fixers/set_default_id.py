from datetime import timezone

from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData


def set_default_id(zettel_raw_data: ZettelRawData) -> None:
    id_str = (
        zettel_raw_data.metadata["date"]
        .astimezone(timezone.utc)
        .strftime(
            "%Y%m%d%H%M%S",
        )
    )
    try:
        zettel_raw_data.metadata["id"] = int(id_str)
    except ValueError as err:
        raise ValueError from err
