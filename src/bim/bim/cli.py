from __future__ import annotations

from pathlib import Path

import click
from buvis.pybase.adapters import console
from buvis.pybase.configuration import Configuration

from bim.commands import CommandFormatNote, CommandImportNote, CommandParseTags

try:
    cfg = Configuration(Path(__file__, "../../config.yaml"))
except FileNotFoundError:
    cfg = Configuration()


@click.group(help="CLI to BUVIS InforMesh")
def cli() -> None:
    pass


@cli.command("import", help="Import a note to zettelkasten")
@click.argument("path_to_note")
def import_note(
    path_to_note: Path,
) -> None:
    if Path(path_to_note).is_file():
        cfg.set_configuration_item("path_note", path_to_note)
        cmd = CommandImportNote(cfg)
        cmd.execute()
    else:
        console.failure(f"{path_to_note} doesn't exist")


@cli.command("format", help="Format a note")
@click.argument("path_to_note")
@click.option(
    "-h",
    "--highlight",
    is_flag=True,
    show_default=True,
    default=False,
    help="Highlight formatted content",
)
@click.option(
    "-d",
    "--diff",
    is_flag=True,
    show_default=True,
    default=False,
    help="Show original and formatted note side by side if different",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(file_okay=True, dir_okay=False, writable=True, resolve_path=True),
)
def format_note(
    path_to_note: Path,
    *,
    highlight: bool,
    diff: bool,
    output: None | Path,
) -> None:
    if output:
        cfg.set_configuration_item("path_output", output)
    cfg.set_configuration_item("is_highlighting_requested", highlight)
    cfg.set_configuration_item("is_diff_requested", diff)

    if Path(path_to_note).is_file():
        cfg.set_configuration_item("path_note", path_to_note)
        cmd = CommandFormatNote(cfg)
        cmd.execute()
    else:
        console.failure(f"{path_to_note} doesn't exist")


@cli.command("parse_tags", help="Parse Obsidian Metadata Extractor tags.json")
@click.argument("path_to_tags_json")
@click.option(
    "-o",
    "--output",
    type=click.Path(file_okay=True, dir_okay=False, writable=True, resolve_path=True),
)
def parse_tags(
    path_to_tags_json: Path,
    *,
    output: None | Path,
) -> None:
    if output:
        cfg.set_configuration_item("path_output", output)

    if Path(path_to_tags_json).is_file():
        cfg.set_configuration_item("path_tags_json", path_to_tags_json)
        cmd = CommandParseTags(cfg)
        cmd.execute()
    else:
        console.failure(f"{path_to_tags_json} doesn't exist")


if __name__ == "__main__":
    cli()
