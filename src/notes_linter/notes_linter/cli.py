from pathlib import Path

import click
from buvis.adapters import ConfigAdapter, console

from notes_linter.commands import CommandPreview

try:
    cfg = ConfigAdapter(Path(__file__, "../../config.yaml"))
except FileNotFoundError:
    cfg = ConfigAdapter()


@click.group(help="CLI tool to lint my notes", invoke_without_command=True)
@click.argument("path_to_note")
def cli(path_to_note: Path):
    if Path(path_to_note).is_file():
        cfg.set_key_value("path_note", path_to_note)
        cmd = CommandPreview(cfg)
        cmd.execute()
    else:
        console.failure(f"{path_to_note} doesn't exist")


if __name__ == "__main__":
    cli()
