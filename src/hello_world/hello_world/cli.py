from pathlib import Path

import click

from buvis.adapters import ConfigAdapter

from hello_world.commands import CommandPrintFiglet

try:
    cfg = ConfigAdapter(Path(__file__,"../../config.yaml"))
    res = cfg.get_key_value("figlet_font")

    if res.is_ok():
        DEFAULT_FONT = res.payload
    else:
        DEFAULT_FONT = 'doom'
except FileNotFoundError:
    cfg = ConfigAdapter()
    DEFAULT_FONT = 'doom'

DEFAULT_TEXT = 'World'

@click.group(help="CLI tool as script proof of concept", invoke_without_command=True)
@click.option("-f","--font", default=DEFAULT_FONT, help="Font to use for stylized printing.")
@click.argument("text", default=DEFAULT_TEXT)
def cli(
    text: str = DEFAULT_TEXT,
    font: str = DEFAULT_FONT,
):
    cfg.set_key_value("font", font)
    cfg.set_key_value("text", text)

    cmd = CommandPrintFiglet(cfg)
    cmd.execute()


if __name__ == "__main__":
    cli()
