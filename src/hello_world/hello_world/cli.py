import re
import sys
from importlib.metadata import distributions, requires
from pathlib import Path

import click
import pyfiglet
from buvis.pybase.configuration import buvis_options, get_settings

from hello_world.commands import CommandPrintFiglet
from hello_world.settings import HelloWorldSettings


@click.group(help="CLI tool as script proof of concept", invoke_without_command=True)
@buvis_options(settings_class=HelloWorldSettings)
@click.option(
    "-f",
    "--font",
    default=None,
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
@click.argument("text", default=None, required=False)
@click.pass_context
def cli(
    ctx: click.Context,
    text: str | None,
    font: str | None,
    *,
    list_fonts: bool = False,
    random_font: bool = False,
    diag: bool = False,
) -> None:
    settings = get_settings(ctx, HelloWorldSettings)

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
        return

    # Resolve font: CLI > settings
    resolved_font = font if font is not None else settings.font
    if random_font:
        import random

        resolved_font = random.choice(pyfiglet.FigletFont.getFonts())  # noqa: S311
        print(f"Random font selected: {resolved_font}")

    if resolved_font not in pyfiglet.FigletFont.getFonts():
        resolved_font = settings.font

    # Resolve text: CLI > settings
    resolved_text = text if text is not None else settings.text

    cmd = CommandPrintFiglet(font=resolved_font, text=resolved_text)
    cmd.execute()


if __name__ == "__main__":
    cli()
