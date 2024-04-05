import importlib, sys, virtualenv, subprocess
from pathlib import Path

class PoetryAdapter:

    @staticmethod
    def run_script(launcher, arguments):
        pkg_name = Path(launcher).stem.replace("-","_")
        pkg_src = Path(launcher,"../../src/",pkg_name).resolve()

        sys.path.insert(0, str(pkg_src))

        venv_dir_stdout = subprocess.run(['poetry', '--directory', pkg_src, 'env','info','--path'], stdout=subprocess.PIPE)
        venv_dir = Path(venv_dir_stdout.stdout.decode('utf-8').strip())

        venv_activator = Path(venv_dir, "Scripts", "activate_this.py")

        # TODO: if venv not found, then I need to run poetry install

        exec(open(venv_activator).read(), {'__file__': venv_activator})

        launcher = importlib.import_module(f"{pkg_name}.cli")

        launcher.cli()
