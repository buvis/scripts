import os

from .console.console import console
from .poetry.poetry import PoetryAdapter

if os.name == "nt":
    from .outlook_local.outlook_local import OutlookLocalAdapter

__all__ = ["console", "PoetryAdapter"]
