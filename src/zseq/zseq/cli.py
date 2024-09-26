from pathlib import Path

import click
from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError

from zseq.commands import CommandGetLast

DEFAULT_PATH_DIR = "/Volumes/photography/photography/src/2024"

try:
    cfg = Configuration(Path(__file__, "../../config.yaml"))
except FileNotFoundError:
    cfg = Configuration()
    DEFAULT_PATH_DIR = "/Volumes/photography/photography/src/2024"
else:
    try:
        DEFAULT_PATH_DIR = str(cfg.get_configuration_item("path_dir", DEFAULT_PATH_DIR))
    except ConfigurationKeyNotFoundError as _:
        DEFAULT_PATH_DIR = "/Volumes/photography/photography/src/2024"

DEFAULT_IS_REPORTING_MISNAMED = False


@click.group(
    help="CLI tool to work with Zettelkasten sequential file naming",
    invoke_without_command=True,
)
@click.option(
    "-p",
    "--path",
    default=DEFAULT_PATH_DIR,
    help="Path to directory containing files following Zettelkasten sequential file naming.",
)
@click.option(
    "-m",
    "--misnamed-reporting",
    is_flag=True,
    show_default=True,
    default=False,
    help="Report files not following Zettelkasten sequential file naming",
)
def cli(
    path: str = DEFAULT_PATH_DIR,
    *,
    misnamed_reporting: bool = DEFAULT_IS_REPORTING_MISNAMED,
) -> None:
    cfg.set_configuration_item("path_dir", path)
    cfg.set_configuration_item("is_reporting_misnamed", misnamed_reporting)

    cmd = CommandGetLast(cfg)
    cmd.execute()


if __name__ == "__main__":
    cli()
