from pathlib import Path

from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError
from buvis_scripts.core.domain import ZettelFactory, ZettelFormatterMarkdown


class CommandPreview:
    def __init__(self: "CommandPreview", cfg: Configuration) -> None:
        try:
            path_note = Path(str(cfg.get_configuration_item("path_note")))
            if not path_note.is_file():
                raise FileNotFoundError
            self.path_note = path_note
        except ConfigurationKeyNotFoundError as e:
            raise FileNotFoundError from e

    def execute(self: "CommandPreview") -> None:
        note = ZettelFactory.create_from_file(self.path_note)
        formatted_md = note.format(ZettelFormatterMarkdown)
        print(formatted_md)
