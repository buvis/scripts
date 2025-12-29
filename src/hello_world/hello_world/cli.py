import re
import sys
from importlib.metadata import distributions, requires
from pathlib import Path

import click
import pyfiglet
from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError

from hello_world.commands import CommandPrintFiglet

DEFAULT_FONT = "doom"

try:
    cfg = Configuration(Path(__file__, "../../config.yaml"))
except FileNotFoundError:
    cfg = Configuration()
    DEFAULT_FONT = "doom"
else:
    try:
        DEFAULT_FONT = str(cfg.get_configuration_item("figlet_font", DEFAULT_FONT))
    except ConfigurationKeyNotFoundError as _:
        DEFAULT_FONT = "doom"

DEFAULT_TEXT = "World"


@click.group(help="CLI tool as script proof of concept", invoke_without_command=True)
@click.option(
    "-f",
    "--font",
    default=DEFAULT_FONT,
    help="Font to use for stylized printing.",
)
@click.option(
    "-l",
    "--list-fonts",
    is_flag=True,
    show_default=True,
    default=False,
    help="List available fonts",
)
@click.option(
    "-r",
    "--random-font",
    is_flag=True,
    show_default=True,
    default=False,
    help="Pick random font",
)
@click.option(
    "--diag",
    is_flag=True,
    default=False,
    help="Print python runtime and dependency info",
)
@click.argument("text", default=DEFAULT_TEXT)
def cli(
    text: str = DEFAULT_TEXT,
    font: str = DEFAULT_FONT,
    *,
    list_fonts: bool = False,
    random_font: bool = False,
    diag: bool = False,
) -> None:
    if diag:
        print(f"Script: {Path(__file__).resolve()}")
        print(f"Python: {sys.executable}")
        print("\nDirect dependencies:")
        reqs = requires("hello-world") or []
        direct_deps = {
            re.split(r"[<>=!~\[;]", r)[0].lower().replace("-", "_") for r in reqs
        }
        for dist in sorted(distributions(), key=lambda d: d.metadata["Name"].lower()):
            name = dist.metadata["Name"]
            normalized = name.lower().replace("-", "_")
            if normalized in direct_deps:
                version = dist.version
                location = dist._path.parent if hasattr(dist, "_path") else "unknown"
                print(f"  {name}=={version} ({location})")
        return

    if list_fonts:
        print("\n".join(sorted(pyfiglet.FigletFont.getFonts())))
    else:
        if random_font:
            import random

            font = random.choice(pyfiglet.FigletFont.getFonts())  # noqa: S311
            print(f"Random font selected: {font}")

        if font in pyfiglet.FigletFont.getFonts():
            cfg.set_configuration_item("font", font)
        else:
            cfg.set_configuration_item("font", DEFAULT_FONT)

        cfg.set_configuration_item("text", text)

        cmd = CommandPrintFiglet(cfg)
        cmd.execute()


if __name__ == "__main__":
    cli()
