"""Common runner for uv tool scripts with local venv fallback."""

import subprocess
import sys
from pathlib import Path


def run(script_file: str, args: list[str] | None = None) -> None:
    """Run from local venv, project source, or installed tool."""
    if args is None:
        args = sys.argv[1:]

    script = Path(script_file).resolve()
    tool_cmd = script.stem
    pkg_name = tool_cmd.replace("-", "_")
    scripts_root = script.parent.parent  # parent of bin/
    project_dir = scripts_root / "src" / pkg_name

    # Check if running from within the scripts repo (dev mode)
    cwd = Path.cwd().resolve()
    in_dev_mode = cwd == scripts_root or scripts_root in cwd.parents

    if in_dev_mode:
        # Dev mode: use local venv or run from source
        venv_bin = project_dir / ".venv" / "bin" / tool_cmd
        if venv_bin.exists():
            result = subprocess.run([venv_bin, *args], check=False)
            sys.exit(result.returncode)

        if project_dir.exists() and (project_dir / "pyproject.toml").exists():
            result = subprocess.run(
                ["uv", "run", "--project", str(project_dir), "-m", pkg_name, *args],
                check=False,
            )
            sys.exit(result.returncode)

        print(f"No venv or project found at {project_dir}", file=sys.stderr)
        sys.exit(1)

    # Production mode: use uv tool run (avoids PATH lookup of wrapper)
    result = subprocess.run(["uv", "tool", "run", tool_cmd, *args], check=False)
    sys.exit(result.returncode)
