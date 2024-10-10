from __future__ import annotations

from pathlib import Path

import click
from buvis.pybase.adapters import console
from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError

from pinger.commands import CommandWait, CommandWaitTimeoutError

DEFAULT_TIMEOUT = 600

try:
    cfg_path = Path(__file__, "../../config.yaml")
    cfg = Configuration(cfg_path)
except FileNotFoundError:
    cfg = Configuration()


@click.group(help="Useful tools around ICMP ping")
def cli() -> None:
    pass


@cli.command("wait", help="Wait for host to be online")
@click.option(
    "-t",
    "--timeout",
    help="Give up waiting after xxx seconds.",
)
@click.argument("host")
def wait(timeout: int | None = None, *, host: str) -> None:
    cfg.set_configuration_item("host", host)

    if timeout:
        cfg.set_configuration_item("wait_timeout", timeout)

    try:
        applied_timeout = cfg.get_configuration_item("wait_timeout")
    except ConfigurationKeyNotFoundError as _:
        cfg.set_configuration_item("wait_timeout", DEFAULT_TIMEOUT)
        applied_timeout = cfg.get_configuration_item("wait_timeout")

    cmd = CommandWait(cfg)
    with console.status(
        f"Waiting for {host} to be online (max {applied_timeout} seconds)"
    ):
        try:
            cmd.execute()
        except CommandWaitTimeoutError as _:
            console.panic(f"Timeout reached when waiting for {host}")
    console.success(f"{host} is now online")


if __name__ == "__main__":
    cli()
