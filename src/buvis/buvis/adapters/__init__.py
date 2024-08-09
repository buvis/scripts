# ATTENTION: don't lint in vim by saving by :w before exiting
from .response import AdapterResponse
from .config.config import cfg, ConfigAdapter
from .console.console import console
from .poetry.poetry import PoetryAdapter
import os

if os.name == "nt":
    from .outlook_local.outlook_local import OutlookLocalAdapter
