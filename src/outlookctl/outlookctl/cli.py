from pathlib import Path

import click
from buvis.pybase.configuration import Configuration

from outlookctl.commands import CommandCreateTimeblock

try:
    cfg = Configuration(Path(__file__, "../../config.yaml"))
except FileNotFoundError:
    cfg = Configuration()


@click.group(help="CLI to Outlook")
def cli() -> None:
    pass


@cli.command("create_timeblock")
def create_timeblock() -> None:
    cmd = CommandCreateTimeblock(cfg)
    cmd.execute()


if __name__ == "__main__":
    cli()
