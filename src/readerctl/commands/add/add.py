from buvis.pybase.adapters import console
from buvis.pybase.configuration import ConfigurationKeyNotFoundError, cfg

from readerctl.adapters import ReaderAPIAdapter


class CommandAdd:
    def __init__(self: "CommandAdd") -> None:
        try:
            token = cfg.get_configuration_item("token")
        except ConfigurationKeyNotFoundError as e:
            console.panic(str(e))
        else:
            self.api = ReaderAPIAdapter(token)

    def execute(self: "CommandAdd", url: str) -> None:
        if self.api:
            res = self.api.add_url(url)

            if res.is_ok():
                console.success(res.payload)
            else:
                console.failure(res.payload)
