from pathlib import Path
from buvis.adapters.config.config import ConfigAdapter


class FCTrackerConfig:

    def __init__(
        self,
        file_path=Path.joinpath(Path.home(), ".config/fctracker/config.yml"),
    ):
        self._config = ConfigAdapter(file_path)

    @property
    def local_currency(self):
        res = self._config.get_key_value("local_currency")
        local_currency_dict = {"code": "CZK", "symbol": "Kč", "precision": 2}

        if res.is_ok() is True:
            for key_val in res.payload:
                for key, val in key_val.items():
                    local_currency_dict[key] = val

        return local_currency_dict

    @property
    def currency(self):
        res = self._config.get_key_value("foreign_currencies")
        currency_dict = {}

        if res.is_ok() is True:
            for currency in res.payload:
                for currency_code, props in currency.items():
                    currency_dict[currency_code] = {}

                    for key_val in props:
                        for key, val in key_val.items():
                            currency_dict[currency_code][key] = val

        return currency_dict


cfg = FCTrackerConfig()
