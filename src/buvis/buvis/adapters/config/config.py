from __future__ import annotations

import os
from pathlib import Path

import yaml

from buvis.adapter_response import AdapterResponse


class ConfigAdapter:
    """
    Manages global runtime configuration for BUVIS scripts.
    Provides functionality to load from YAML file, access, and modify configuration settings.

    If no configuration file path is provided, then it tries to find the path from the `BUVIS_CONFIG_FILE`
    environment variable. If the environment variable is not set, it defaults to `~/.config/buvis/config.yaml`.
    """

    def __init__(self: ConfigAdapter, file_path: Path | None = None) -> None:
        """
        Initializes the ConfigAdapter with a specified YAML configuration file.

        :param file_path: Optional path to the configuration file. Defaults to '~/.config/buvis/config.yaml'.
        :type file_path: Path | None
        :raises FileNotFoundError: If the configuration file does not exist.
        """
        self._config_dict = {}

        existing_file_path = self._determine_config_path(file_path)

        if existing_file_path is not None:
            self.path_config_file = existing_file_path
            self._load_configuration()

    def _determine_config_path(
        self: ConfigAdapter,
        file_path: Path | None,
    ) -> Path | None:
        """
        Determines the absolute path to the configuration file.

        This method attempts to resolve the configuration file path based on the provided `file_path`.
        If `file_path` is provided and exists, it returns the absolute path. If the file does not exist,
        it raises a FileNotFoundError.

        If no `file_path` is provided, the method tries to find the path from the 'BUVIS_CONFIG_FILE'
        environment variable. If the environment variable is not set, it defaults to '~/.config/buvis/config.yaml'.
        If the resolved path from the environment or default exists, it returns the absolute path.
        If it does not exist, it returns None.

        :param file_path: Optional path provided by the user.
        :type file_path: Path | None
        :return: The absolute path to the configuration file or None if the default path does not exist.
        :rtype: Path | None
        :raises FileNotFoundError: If the provided `file_path` does not exist.
        """
        if file_path is not None:
            if file_path.exists():
                return file_path.absolute()
            message = f"The configuration file at {file_path} was not found."
            raise FileNotFoundError(message)

        # Try getting the path from environment or default to home directory
        alternative_file_path = Path(
            os.getenv("BUVIS_CONFIG_FILE", Path.home() / ".config/buvis/config.yaml"),
        )
        if alternative_file_path.exists():
            return alternative_file_path.absolute()

        return None

    def _load_configuration(self: ConfigAdapter) -> None:
        """
        Loads the configuration from the YAML file.
        """
        with self.path_config_file.open("r") as file:
            self._config_dict = yaml.safe_load(file) or {}

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