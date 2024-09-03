from pathlib import Path

import click
from buvis_scripts.core.adapters import ConfigAdapter

from outlookctl.commands import CommandCreateTimeblock

try:
    cfg = ConfigAdapter(Path(__file__, "../../config.yaml"))
except FileNotFoundError:
    cfg = ConfigAdapter()


@click.group(help="CLI to Outlook")
def cli():
    pass


@cli.command("create_timeblock")
def create_timeblock():
    cmd = CommandCreateTimeblock(cfg)
    cmd.execute()


if __name__ == "__main__":
    cli()
