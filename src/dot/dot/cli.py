from __future__ import annotations

from pathlib import Path

import click
from buvis.pybase.adapters import console, logging_to_console
from buvis.pybase.configuration import Configuration
from buvis.pybase.filesystem import DirTree

from dot.commands import CommandAdd, CommandStatus

path_cfg = Path(__file__, "../../config.yaml").resolve()

try:
    cfg = Configuration(path_cfg)
except FileNotFoundError:
    console.panic(f"Defaults configuration not found in {path_cfg}")


@click.group(help="CLI for bare repo dotfiles")
def cli() -> None:
    pass


@cli.command("status", help="Report status")
def status() -> None:
    with logging_to_console():
        cmd = CommandStatus(cfg)
        cmd.execute()


@cli.command("add", help="Add changes")
@click.argument("file_path", required=False)
def add(file_path: Path | None) -> None:
    cfg.set_configuration_item("add_file_path", file_path)
    with logging_to_console():
        cmd = CommandAdd(cfg)
        cmd.execute()


if __name__ == "__main__":
    cli()
