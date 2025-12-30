#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["buvis-pybase"]
# ///
"""Zero-dependency bootstrap + runner for uv tool wrappers.

Bootstrap (`run()`): uses installed tool's Python when available,
falls back to `uv run --script` for auto-install.

Runner (`__main__`): invokes UvToolManager.run with buvis-pybase.
"""

import subprocess
import sys
from pathlib import Path


def _get_uv_tools_dir() -> Path | None:
    """Get uv tools directory portably."""
    result = subprocess.run(
        ["uv", "tool", "dir"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return Path(result.stdout.strip())
    return None


def run(script_path: str) -> None:
    """Bootstrap and run a uv tool via UvToolManager."""
    script = Path(script_path).resolve()
    tool_name = script.stem
    args = sys.argv[1:]
    runner = script.parent / "_script_runner.py"

    tools_dir = _get_uv_tools_dir()
    tool_python = tools_dir / tool_name / "bin" / "python" if tools_dir else None

    if tool_python and tool_python.exists():
        # Fast path: use installed tool's Python
        result = subprocess.run([str(tool_python), str(runner), str(script), *args], check=False)
    else:
        # First run: bootstrap via uv run --script
        result = subprocess.run(["uv", "run", "--script", str(runner), str(script), *args], check=False)

    sys.exit(result.returncode)


if __name__ == "__main__":
    from buvis.pybase.adapters.uv import UvToolManager

    UvToolManager.run(sys.argv[1], sys.argv[2:])
