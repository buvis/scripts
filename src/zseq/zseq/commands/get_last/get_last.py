from pathlib import Path

from buvis.pybase.adapters import console
from buvis.pybase.configuration import Configuration, ConfigurationKeyNotFoundError

from zseq.shared import ZseqFilename

DEFAULT_PATH_DIR = Path("/Volumes/photography/photography/src/2024")
DEFAULT_IS_REPORTING_MISNAMED = False


class CommandGetLast:
    path_dir: Path
    is_reporting_misnamed: bool

    def __init__(self: "CommandGetLast", cfg: Configuration) -> None:
        try:
            self.path_dir = Path(
                str(cfg.get_configuration_item("path_dir", DEFAULT_PATH_DIR)),
            )
        except ConfigurationKeyNotFoundError as _:
            self.path_dir = DEFAULT_PATH_DIR
        self.path_dir = Path(str(self.path_dir))

        if not self.path_dir.is_dir():
            msg = f"{self.path_dir} is not a directory"
            raise ValueError(msg)

        try:
            self.is_reporting_misnamed = bool(
                cfg.get_configuration_item(
                    "is_reporting_misnamed",
                    DEFAULT_IS_REPORTING_MISNAMED,
                ),
            )
        except ConfigurationKeyNotFoundError as _:
            self.is_reporting_misnamed = DEFAULT_IS_REPORTING_MISNAMED

    def execute(self: "CommandGetLast") -> None:
        seqs = [
            ZseqFilename.get_seq_from_zettelseq(f.stem)
            for f in self.path_dir.iterdir()
            if ZseqFilename.is_zettelseq(
                f,
                is_reporting_fails=self.is_reporting_misnamed,
            )
        ]

        if seqs:
            console.success(
                f"Last sequence number in {self.path_dir.absolute()} is {max(seqs)}",
            )
        else:
            console.failure(
                f"No files following zettelseq naming scheme found in {self.path_dir.absolute()}",
            )
