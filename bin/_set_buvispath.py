import sys
from pathlib import Path


def set_buvispath() -> None:
    bin_dir = Path(__file__).parent
    src_dir = Path(bin_dir / ".." / "src").resolve()
    buvis_dir = Path(src_dir / "buvis").resolve()
    sys.path.insert(0, str(src_dir))
    sys.path.insert(0, str(buvis_dir))
