"""Zero-dependency bootstrap for uv tool wrappers.

Uses installed tool's Python to run UvToolManager.run, avoiding ephemeral environments.
Falls back to uv run --script for auto-install when tool not installed.
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

    tools_dir = _get_uv_tools_dir()
    tool_python = tools_dir / tool_name / "bin" / "python" if tools_dir else None

    if tool_python and tool_python.exists():
        # Use installed tool's Python (has buvis-pybase)
        runner = script.parent / "_runner.py"
        result = subprocess.run(
            [str(tool_python), str(runner), str(script), *args],
            check=False,
        )
        sys.exit(result.returncode)

    # Tool not installed - bootstrap via uv run --script
    result = subprocess.run(
        [
            "uv",
            "run",
            "--script",
            str(script.parent / "_fallback.py"),
            str(script),
            *args,
        ],
        check=False,
    )
    sys.exit(result.returncode)