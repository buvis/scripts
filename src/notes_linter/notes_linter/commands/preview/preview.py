from pathlib import Path

from buvis.pybase.filesystem import get_file_creation_datetime
from buvis_scripts.core.adapters import ConfigAdapter
from buvis_scripts.core.domain import ZettelFactory, ZettelFormatterMarkdown


class CommandPreview:
    def __init__(self: "CommandPreview", cfg: ConfigAdapter) -> None:
        res = cfg.get_configuration_item("path_note")

        if res.is_ok() and Path(str(res.payload)).is_file():
            self.path_note = Path(str(res.payload))
        else:
            raise FileNotFoundError

    def execute(self: "CommandPreview") -> None:
        note = ZettelFactory.create_from_file(self.path_note)
        formatted_md = note.format(ZettelFormatterMarkdown)
        print(formatted_md)
