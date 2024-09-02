from buvis_scripts.core.domain.entity.zettel.zettel_data import ZettelData
from buvis_scripts.core.shared import StrConv


def fix_title_format(zettel_data: ZettelData) -> None:
    zettel_data.metadata["title"] = StrConv.replace_abbreviations(
        text=zettel_data.metadata["title"],
        level=0,
    )
