from pathlib import Path

from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError
from doogat.core import (
    MarkdownZettelFormatter,
    MarkdownZettelRepository,
    PrintZettelUseCase,
    ReadDoogatUseCase,
)


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
        repo = MarkdownZettelRepository()
        reader = ReadDoogatUseCase(repo)
        formatter = MarkdownZettelFormatter()
        printer = PrintZettelUseCase(formatter)
        note = reader.execute(str(self.path_note))
        printer.execute(note.get_data())
