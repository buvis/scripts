import datetime
from pathlib import Path

from buvis.adapters import console


class ZseqFilename:

    def is_zettelseq(filename: Path, is_reporting_fails: bool = False):
        try:
            datetime.datetime.strptime(filename.stem[:14],
                                       "%Y%m%d%H%M%S").date()
        except ValueError:
            if is_reporting_fails:
                console.failure(
                    f"{filename.absolute()} is not in zettelseq scheme")

            return False

        return True

    def get_seq_from_zettelseq(zettelseq):
        return int(str(zettelseq[15:19]))
