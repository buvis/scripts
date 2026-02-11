#!/usr/bin/env python3
"""Toggle local development dependencies."""

import re
import shutil
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONFIG = Path(__file__).parent / "deps.toml"


def _clean_envs():
    """Remove stale project venvs, lockfiles, and uv ephemeral caches."""
    for venv in (ROOT / "src").glob("*/.venv"):
        shutil.rmtree(venv)
        print(f"  rm {venv.parent.name}/.venv")
    for lock in (ROOT / "src").glob("*/uv.lock"):
        lock.unlink()
        print(f"  rm {lock.parent.name}/uv.lock")
    cache_dir = Path.home() / ".cache" / "uv" / "environments-v2"
    if cache_dir.exists():
        for p in cache_dir.glob("*-*"):
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    print("Cleaned stale envs")


def load_deps():
    """Load dependencies from config file."""
    with open(CONFIG, "rb") as f:
        return tomllib.load(f).get("deps", {})


def enable():
    deps = load_deps()

    for f in (ROOT / "bin").iterdir():
        if f.is_file() and not f.suffix:
            content = f.read_text()
            updated = False
            for dep, path in deps.items():
                if dep in content and f"# {dep} = " not in content:
                    # Path from bin/ to dep (one level up from root)
                    bin_path = f"../{path}"
                    source_line = f'\n#\n# [tool.uv.sources]\n# {dep} = {{ path = "{bin_path}" }}'
                    content = content.replace(f'# dependencies = ["{dep}"]', f'# dependencies = ["{dep}"]{source_line}')
                    # For existing [tool.uv.sources], add new dep
                    if "[tool.uv.sources]" in content and f"# {dep} = " not in content:
                        content = re.sub(
                            r"(# \[tool\.uv\.sources\])", f'\\1\n# {dep} = {{ path = "{bin_path}" }}', content
                        )
                    updated = True
            if updated:
                # Ensure closing tag is correct
                content = re.sub(r"\n# ///\n", "\n# ///\n", content)
                f.write_text(content)
                print(f"+ {f.name}")

    for f in (ROOT / "src").glob("*/pyproject.toml"):
        content = f.read_text()
        updated = False
        for dep, path in deps.items():
            if dep in content and f'"{dep}" = {{ path' not in content:
                # Path from src/*/ to dep (two levels up from root)
                src_path = f"../../{path}"
                if "[tool.uv.sources]" in content:
                    # Add to existing section
                    content = re.sub(
                        r"(\[tool\.uv\.sources\])",
                        f'\\1\n"{dep}" = {{ path = "{src_path}", editable = true }}',
                        content,
                    )
                else:
                    # Create new section before [project.scripts]
                    source_block = f'[tool.uv.sources]\n"{dep}" = {{ path = "{src_path}", editable = true }}\n\n'
                    content = content.replace("[project.scripts]", source_block + "[project.scripts]")
                updated = True
        if updated:
            f.write_text(content)
            print(f"+ {f.parent.name}/pyproject.toml")

    _clean_envs()
    print("Dev mode enabled")


def disable():
    for f in (ROOT / "bin").iterdir():
        if f.is_file() and not f.suffix:
            content = f.read_text()
            if "[tool.uv.sources]" in content:
                # Remove entire [tool.uv.sources] block from inline script metadata
                content = re.sub(
                    r'\n#\n# \[tool\.uv\.sources\]\n(# [^\n]+ = \{ path = "[^"]*" \}\n)+# ///', "\n# ///", content
                )
                f.write_text(content)
                print(f"- {f.name}")

    for f in (ROOT / "src").glob("*/pyproject.toml"):
        content = f.read_text()
        if "[tool.uv.sources]" in content:
            # Remove entire [tool.uv.sources] section
            content = re.sub(
                r'\[tool\.uv\.sources\]\n("[^"]*" = \{ path = "[^"]*", editable = true \}\n)+\n', "", content
            )
            f.write_text(content)
            print(f"- {f.parent.name}/pyproject.toml")

    _clean_envs()
    print("Prod mode enabled")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("enable", "disable"):
        print("Usage: devmode.py enable|disable")
        sys.exit(1)

    {"enable": enable, "disable": disable}[sys.argv[1]]()
