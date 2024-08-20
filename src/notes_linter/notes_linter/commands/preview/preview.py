from pathlib import Path

from buvis.adapters import ConfigAdapter
from buvis.domain import Zettel


class CommandPreview:
    def __init__(self: "CommandPreview", cfg: ConfigAdapter) -> None:
        res = cfg.get_key_value("path_note")

        if res.is_ok() and Path(str(res.payload)).is_file():
            self.path_note = Path(str(res.payload))
        else:
            raise FileNotFoundError

    def execute(self: "CommandPreview") -> None:
        note = Zettel.create_from_file(self.path_note)
        formatted_md = note.to_formatted_markdown()
        print(formatted_md)
