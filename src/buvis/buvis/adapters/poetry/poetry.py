import importlib
import runpy
import subprocess
import sys
from pathlib import Path


class PoetryAdapter:
    @staticmethod
    def run_script(launcher, arguments):
        pkg_name = Path(launcher).stem.replace("-", "_")
        pkg_src = Path(launcher, "../../src/", pkg_name).resolve()

        sys.path.insert(0, str(pkg_src))

        venv_activator = PoetryAdapter.get_activator_path(pkg_src)

        if not venv_activator.is_file():
            subprocess.run(
                ["poetry", "--directory", pkg_src, "install"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )
            venv_activator = PoetryAdapter.get_activator_path(pkg_src)

        if venv_activator.is_file():
            # Activate package's virtual environment
            runpy.run_path(str(venv_activator))

            launcher = importlib.import_module(f"{pkg_name}.cli")
            launcher.cli(arguments)
        else:
            print(
                f"Script preparation failed. Make sure `poetry install` can complete successfully in {pkg_src}."
            )

    @staticmethod
    def get_activator_path(directory):
        venv_dir_stdout = subprocess.run(
            ["poetry", "--directory", directory, "env", "info", "--path"],
            stdout=subprocess.PIPE,
        )
        venv_dir = Path(venv_dir_stdout.stdout.decode("utf-8").strip())
        return Path(venv_dir, "bin", "activate_this.py")
