from buvis_scripts.core.adapters import console

from zseq.shared import ZseqFilename


class CommandGetLast:
    def __init__(self, cfg):
        res = cfg.get_configuration_item("path_dir")

        if res.is_ok():
            self.path_dir = res.payload
        else:
            console.panic(res.payload)

        res = cfg.get_configuration_item("is_reporting_misnamed")

        if res.is_ok():
            self.is_reporting_misnamed = res.payload
        else:
            self.is_reporting_misnamed = False

    def execute(self):
        seqs = [
            ZseqFilename.get_seq_from_zettelseq(f.stem)
            for f in self.path_dir.iterdir()
            if ZseqFilename.is_zettelseq(f, self.is_reporting_misnamed)
        ]

        if seqs:
            console.success(
                f"Last sequence number in {self.path_dir.absolute()} is {max(seqs)}"
            )
        else:
            console.failure(
                f"No files following zettelseq naming scheme found in {self.path_dir.absolute()}"
            )
