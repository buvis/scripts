#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["buvis-pybase"]
# ///
"""Fallback for first-time tool install. Only runs when tool not yet installed."""

import sys

from buvis.pybase.adapters.uv import UvToolManager

if __name__ == "__main__":
    script_path = sys.argv[1]
    args = sys.argv[2:]
    UvToolManager.run(script_path, args)
