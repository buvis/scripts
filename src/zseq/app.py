from pathlib import Path
from typing import Annotated

from buvis.adapters import cfg
from cyclopts import App, Parameter, validators

from zseq.commands import CommandGetLast

app = App(help="CLI tool to manage work with Zettelkasten sequences")


@app.command
def get_last(
    path: Annotated[
        Path, Parameter(name=["--path", "-p"], validator=validators.Path(exists=True))
    ],
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

    cfg.set_configuration_item("path_dir", Path(path))
    cfg.set_configuration_item("is_reporting_misnamed", misnamed)

    cmd = CommandGetLast(cfg)
    cmd.execute()


if __name__ == "__main__":
    app()
