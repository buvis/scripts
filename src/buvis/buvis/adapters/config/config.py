from __future__ import annotations

from pathlib import Path

import yaml

from buvis.adapter_response import AdapterResponse


class ConfigAdapter:
    """
    Manages configuration settings stored in a YAML file.
    Provides functionality to load, access, and modify configuration settings.
    """

    def __init__(self: ConfigAdapter, file_path: Path | None = None) -> None:
        """
        Initializes the ConfigAdapter with a specified YAML configuration file.

        :param file_path: Optional path to the configuration file. Defaults to '~/.config/buvis/config.yaml'.
        :type file_path: Path | None
        :raises FileNotFoundError: If the configuration file does not exist.
        """
        self._config_dict = {}
        self.path_config_file = self._determine_config_path(file_path)

        self._load_configuration()

    def _determine_config_path(self: ConfigAdapter, file_path: Path | None) -> Path:
        """
        Determines the absolute path to the configuration file.
        When no path is provided, the defaults to '~/.config/buvis/config.yaml'.

        :param file_path: Optional path provided by the user.
        :type file_path: Path | None
        :return: The absolute path to the configuration file.
        :rtype: Path
        """
        if file_path is None:
            file_path = Path.home() / ".config/buvis/config.yaml"
        return Path(file_path).absolute()

    def _load_configuration(self: ConfigAdapter) -> None:
        """
        Loads the configuration from the YAML file.

        :raises FileNotFoundError: If the configuration file does not exist.
        """
        if self.path_config_file.exists():
            with self.path_config_file.open("r") as file:
                self._config_dict = yaml.safe_load(file) or {}
        else:
            message = (
                f"The configuration file at {self.path_config_file} was not found."
            )
            raise FileNotFoundError(message)

    def set_configuration_item(self: ConfigAdapter, key: str, value: object) -> None:
        """
        Sets or updates a configuration item.

        :param key: The configuration item key.
        :type key: str
        :param value: The value to associate with the key.
        :type value: object
        """
        self._config_dict[key] = value

    def get_configuration_item(
        self: ConfigAdapter,
        key: str,
        default: object | None = None,
    ) -> AdapterResponse:
        """
        Retrieves a configuration item by key.

        :param key: The configuration item key to retrieve.
        :type key: str
        :param default: Optional default value to use if no value found.
        :type default: object | None
        :return: Contains the configuration value or an error message if not found.
        :rtype: AdapterResponse
        """
        if key in self._config_dict:
            return AdapterResponse(payload=self._config_dict[key])

        if default:
            return AdapterResponse(payload=default)

        return AdapterResponse(404, f"{key} not found in configuration.")


cfg = ConfigAdapter()
