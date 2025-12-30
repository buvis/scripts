"""Runner for installed tools. Called by _bootstrap.py.

No inline deps needed - runs with tool's Python which has buvis-pybase.
"""

import sys

from buvis.pybase.adapters.uv import UvToolManager

if __name__ == "__main__":
    UvToolManager.run(sys.argv[1], sys.argv[2:])
