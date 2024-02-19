from cyclopts import App, Parameter, validators
from typing import Annotated
from pathlib import Path

from buvis.adapters import cfg

from zseq.commands import CommandGetLast

app = App(help="CLI tool to manage work with Zettelkasten sequences")


@app.command
def get_last(
    path: Annotated[Path,
                    Parameter(name=["--path", "-p"],
                              validator=validators.Path(exists=True))],
    misnamed: Annotated[bool, Parameter(name=["--misnamed", "-m"])] = False,
):
    """Get last Zettelkasten sequence number in a directory.

    Parameters
    ----------
    path:
        Path to directory.
    misnamed:
        List files not following zettelseq naming scheme.
    """

    cfg.set_key_value("path_dir", Path(path))
    cfg.set_key_value("is_reporting_misnamed", misnamed)

    cmd = CommandGetLast(cfg)
    cmd.execute()


if __name__ == "__main__":
    app()
