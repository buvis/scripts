from pathlib import Path

from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError


class FCTrackerConfig:
    def __init__(
        self: "FCTrackerConfig",
        file_path=Path.joinpath(Path.home(), ".config/fctracker/config.yml"),
    ) -> None:
        self._config = Configuration(file_path)

    @property
    def local_currency(self: "FCTrackerConfig") -> dict:
        try:
            local_currency_config = self._config.get_configuration_item(
                "local_currency"
            )
        except ConfigurationKeyNotFoundError as _:
            local_currency_config = {}

        local_currency_dict = {"code": "CZK", "symbol": "Kč", "precision": 2}

        for key_val in local_currency_config:
            for key, val in key_val.items():
                local_currency_dict[key] = val

        return local_currency_dict

    @property
    def currency(self: "FCTrackerConfig") -> dict:
        try:
            currencies_config = self._config.get_configuration_item(
                "foreign_currencies"
            )
        except ConfigurationKeyNotFoundError as _:
            currencies_config = {}

        currency_dict = {}

        for currency in currencies_config:
            for currency_code, props in currency.items():
                currency_dict[currency_code] = {}

                for key_val in props:
                    for key, val in key_val.items():
                        currency_dict[currency_code][key] = val

        return currency_dict

    @property
    def transactions_dir(self: "FCTrackerConfig") -> Path:
        try:
            transactions_dir = str(
                self._config.get_configuration_item("transactions_dir"),
            )
        except ConfigurationKeyNotFoundError as e:
            raise FileNotFoundError from e
        else:
            return Path(transactions_dir.replace("~", f"{Path.home()}"))


cfg = FCTrackerConfig()
