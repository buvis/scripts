from pathlib import Path

import click
from buvis.pybase.adapters import console, logging_to_console
from buvis.pybase.configuration import Configuration
from buvis.pybase.filesystem import DirTree

from muc.commands import CommandLimit, CommandTidy

ALERT_FILE_COUNT = 100
ALERT_DIR_DEPTH = 3

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


@cli.command("tidy", help="Tidy directory")
@click.argument("directory")
def tidy(directory: Path) -> None:
    path_directory = Path(directory).resolve()

    if path_directory.is_dir():
        cfg.set_configuration_item("tidy_directory", path_directory)
    else:
        console.panic(f"{path_directory} isn't a directory")

    file_count = DirTree.count_files(path_directory)
    max_depth = DirTree.get_max_depth(path_directory)

    if file_count > ALERT_FILE_COUNT or max_depth > ALERT_DIR_DEPTH:
        message = (
            f"Warning: The directory contains {file_count} files "
            f"and has a maximum depth of {max_depth}. "
            "Do you want to proceed?"
        )
        if not user_confirmation(message):
            console.panic("Operation cancelled by user.")

    with logging_to_console():
        cmd = CommandTidy(cfg)
        cmd.execute()


def user_confirmation(message: str) -> bool:
    """
    Ask for user confirmation.

    :param message: Message to display to the user
    :type message: str
    :return: True if user confirms, False otherwise
    :rtype: bool
    """
    while True:
        response = input(f"{message} (y/n): ").lower().strip()
        if response in ["y", "yes"]:
            return True
        if response in ["n", "no"]:
            return False
        print("Please answer with 'y' or 'n'.")


if __name__ == "__main__":
    cli()
