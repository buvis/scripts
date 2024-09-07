from pathlib import Path

import buvis_scripts.core.domain as entities
from buvis.pybase.formatting import StringOperator

from .zettel_parser import ZettelParser


class ZettelFactory:
    @staticmethod
    def create_from_file(file_path: Path) -> entities.Zettel:
        zettel = entities.Zettel()
        zettel_data = ZettelParser.from_file(file_path)
        zettel.load(zettel_data)
        zettel_type = getattr(zettel, "type", "")

        if zettel_type in ("note", ""):  # generic Zettel
            return zettel

        # try downcasting to more specific Zettel type
        class_name = StringOperator.camelize(zettel_type) + "Zettel"

        try:
            entity_class = getattr(entities, class_name)
        except AttributeError:
            return zettel
        else:
            downcasted_zettel = entity_class()
            downcasted_zettel.load(zettel_data)
            return downcasted_zettel
