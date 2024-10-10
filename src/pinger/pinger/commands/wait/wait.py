import time

from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError
from ping3 import ping

from pinger.commands.wait.exceptions import CommandWaitTimeoutError

DEFAULT_IP = "127.0.0.1"
DEFAULT_TIMEOUT = 600


class CommandWait:
    def __init__(self: "CommandWait", cfg: Configuration) -> None:
        try:
            self.host = cfg.get_configuration_item("host", DEFAULT_IP)
        except ConfigurationKeyNotFoundError as _:
            self.host = DEFAULT_IP
        try:
            self.timeout = int(
                cfg.get_configuration_item("wait_timeout", DEFAULT_TIMEOUT)
            )
        except ConfigurationKeyNotFoundError as _:
            self.timeout = DEFAULT_TIMEOUT

    def execute(self: "CommandWait") -> None:
        start_time = time.time()
        while True:
            response = ping(self.host, timeout=1)
            if response:
                break
            if time.time() - start_time > self.timeout:
                raise CommandWaitTimeoutError
            time.sleep(1)
