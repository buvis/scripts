from pathlib import Path

import click
from buvis.pybase.adapters import console
from buvis.pybase.configuration import Configuration

from muc.commands import CommandLimit

path_cfg = Path(__file__, "../../config.yaml").resolve()

try:
    cfg = Configuration(path_cfg)
except FileNotFoundError:
    console.panic(f"Defaults configuration not found in {path_cfg}")


@click.group(help="Tools for music collection management")
def cli() -> None:
    pass


@cli.command("limit", help="Limit audio file")
@click.option(
    "-o",
    "--output",
    default=Path(Path.cwd() / "transcoded"),
    help="Transcoded files output directory.",
)
@click.argument("source_directory")
def limit(source_directory: Path, output: Path) -> None:
    path_source = Path(source_directory).resolve()

    if path_source.is_dir():
        cfg.set_configuration_item("limit_path_source", path_source)
    else:
        console.panic(f"{source_directory} isn't a directory")

    path_output = Path(output).resolve()
    path_output.mkdir(exist_ok=True)
    cfg.set_configuration_item("limit_path_output", path_output)
    cmd = CommandLimit(cfg)
    cmd.execute()


if __name__ == "__main__":
    cli()
