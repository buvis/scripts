import datetime
from pathlib import Path

from buvis.pybase.adapters import console


class ZseqFilename:
    @staticmethod
    def is_zettelseq(filename: Path, *, is_reporting_fails: bool = False) -> bool:
        try:
            datetime.datetime.strptime(
                filename.stem[:14],
                "%Y%m%d%H%M%S",
            ).astimezone().date()
        except ValueError:
            if is_reporting_fails:
                console.failure(f"{filename.absolute()} is not in zettelseq scheme")

            return False

        return True

    @staticmethod
    def get_seq_from_zettelseq(zettelseq: str) -> int:
        return int(str(zettelseq[15:19]))
