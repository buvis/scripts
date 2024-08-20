from datetime import datetime, timezone

from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData


def set_default_date(zettel_raw_data: ZettelRawData) -> None:
    zettel_raw_data.metadata["date"] = datetime.now(timezone.utc)
