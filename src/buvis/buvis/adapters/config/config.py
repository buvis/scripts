from __future__ import annotations

from pathlib import Path

import yaml

from buvis.adapter_response import AdapterResponse


class ConfigAdapter:
    def __init__(self: ConfigAdapter, file_path: Path | None = None) -> None:
        self.config_dict = {}

        if file_path is None:
            file_path = Path.home() / ".config/buvis/config.yaml"

        self.path_config_file = Path(file_path).absolute()

        if self.path_config_file.exists():
            with self.path_config_file.open("r") as file:
                self.config_dict = yaml.safe_load(file)
        else:
            raise FileNotFoundError

    def set_key_value(self: ConfigAdapter, key: str, value: object) -> None:
        self.config_dict[key] = value

    def get_key_value(self: ConfigAdapter, key: str) -> AdapterResponse:
        if self.config_dict.get(key, ""):
            return AdapterResponse(payload=self.config_dict[key])

        return AdapterResponse(404, f"{key} not found in config store")


cfg = ConfigAdapter()
