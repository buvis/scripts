import importlib
import os
import site
import subprocess
import sys
from pathlib import Path


class PoetryAdapter:
    @staticmethod
    def run_script(launcher, arguments):
        pkg_name = Path(launcher).stem.replace("-", "_")
        pkg_src = Path(launcher, "../../src/", pkg_name).resolve()

        sys.path.insert(0, str(pkg_src))

        venv_dir_stdout = subprocess.run(
            ["poetry", "--directory", pkg_src, "env", "info", "--path"],
            stdout=subprocess.PIPE,
        )
        base = Path(venv_dir_stdout.stdout.decode("utf-8").strip())
        bin_dir = Path(base, "bin")

        os.environ["PATH"] = os.pathsep.join(
            [
                str(bin_dir),
                *os.environ.get("PATH", "").split(os.pathsep),
            ]
        )
        os.environ["VIRTUAL_ENV"] = str(
            base,
        )
        os.environ["VIRTUAL_ENV_PROMPT"] = "__VIRTUAL_PROMPT__" or base.name

        prev_length = len(sys.path)
        for lib in "__LIB_FOLDERS__".split(os.pathsep):
            path = os.path.realpath(Path(bin_dir, lib))
            try:
                site.addsitedir(path.decode("utf-8") if "__DECODE_PATH__" else path)
            except AttributeError:
                site.addsitedir(path)
        sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]

        sys.real_prefix = sys.prefix
        sys.prefix = base

        # TODO: if venv not found, then I need to run poetry install

        launcher = importlib.import_module(f"{pkg_name}.cli")

        launcher.cli(arguments)
