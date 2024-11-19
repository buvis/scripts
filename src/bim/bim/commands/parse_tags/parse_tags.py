import json
from pathlib import Path

from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError


class CommandParseTags:
    def __init__(self: "CommandParseTags", cfg: Configuration) -> None:
        try:
            path_tags_json = Path(str(cfg.get_configuration_item("path_tags_json")))
            if not path_tags_json.is_file():
                raise FileNotFoundError
            self.path_tags_json = path_tags_json
        except ConfigurationKeyNotFoundError as e:
            raise FileNotFoundError from e

        try:
            self.path_output = Path(
                str(cfg.get_configuration_item("path_output")),
            ).resolve()
        except ConfigurationKeyNotFoundError as _:
            self.path_output = None

    def execute(self: "CommandParseTags") -> None:
        data = json.loads(self.path_tags_json.read_text())
        tags = [item["tag"] for item in data]
        unique_sorted_tags = sorted(set(tags))

        if self.path_output:
            self.path_output.write_text("\n".join(unique_sorted_tags))
        else:
            print("\n".join(unique_sorted_tags))
