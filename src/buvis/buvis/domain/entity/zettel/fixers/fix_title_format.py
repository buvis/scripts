from buvis.domain.entity.zettel.zettel_raw_data import ZettelRawData
from buvis.shared import StrConv


def fix_title_format(zettel_raw_data: ZettelRawData) -> None:
    zettel_raw_data.metadata["title"] = StrConv.replace_abbreviations(
        text=zettel_raw_data.metadata["title"],
        level=0,
    )
