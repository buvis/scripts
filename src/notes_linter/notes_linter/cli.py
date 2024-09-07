from pathlib import Path

import click
from buvis.pybase.adapters import console
from buvis.pybase.configuration import Configuration

from notes_linter.commands import CommandPreview

try:
    cfg = Configuration(Path(__file__, "../../config.yaml"))
except FileNotFoundError:
    cfg = Configuration()


@click.group(help="CLI tool to lint my notes", invoke_without_command=True)
@click.argument("path_to_note")
def cli(path_to_note: Path) -> None:
    if Path(path_to_note).is_file():
        cfg.set_configuration_item("path_note", path_to_note)
        cmd = CommandPreview(cfg)
        cmd.execute()
    else:
        console.failure(f"{path_to_note} doesn't exist")


if __name__ == "__main__":
    cli()
