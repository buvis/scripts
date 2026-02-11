# CLAUDE.md

BUVIS scripts monorepo. CLI tools built on buvis-pybase, each as an independent uv-managed package.

## Quick Start

```bash
uv sync --all-groups                        # install deps (per package: cd src/<name>)
pre-commit install                          # setup hooks
uv run --with pytest pytest                 # run tests (from package dir)
```

## Architecture

```text
bin/                    # Entry-point wrappers (shims that call src/ packages)
src/
├── bim/                # BUVIS InfoMesh CLI (doogat integration)
├── dot/                # Dotfiles manager
├── fctracker/          # Foreign currency account tracker
├── hello_world/        # Sample script template
├── muc/                # Music collection tools
├── outlookctl/         # Outlook CLI
├── pinger/             # ICMP ping utilities
├── readerctl/          # Readwise Reader CLI
└── zseq/               # Zettelsequence utilities
dev/
├── devmode.py          # Toggle local dependency mode
├── deps.toml           # Local dependency mappings
├── finish-dev          # Switch back to PyPI deps
└── start-dev           # Switch to local deps
```

**Key patterns:**

- **Independent packages**: each `src/<name>/` has its own `pyproject.toml`, venv, and tests
- **Shared base**: all packages depend on `buvis-pybase` for CLI scaffolding, config, adapters
- **Dev mode**: `start-dev` / `finish-dev` toggle between local and PyPI dependencies
- **Bin shims**: `bin/<name>` scripts run `uv run --from src/<name> <name>` for global access

## Code Conventions

**Type hints** - modern style, no `Optional`:

```python
from __future__ import annotations
def foo(path: Path | None = None) -> list[str]: ...
```

**Imports**:

- Explicit `__all__` in `__init__.py`
- `TYPE_CHECKING` guards for type-only imports

**Docstrings**: Google format

**CLI pattern**: Click-based, inheriting from `BuvisCommand`:

```python
@click.command()
@buvis_options
@click.pass_context
def cli(ctx: click.Context) -> None:
    command = MyCommand(ctx.obj["settings"])
    command.execute()
```

## Testing

- pytest + pytest-mock + pytest-cov
- Tests in `src/<name>/tests/` mirror package structure
- Mock subprocess calls heavily
- Class-based test organization
- **No unused imports/variables**: don't add `noqa: F401` or `noqa: F841` - either use the import/variable or remove it

```python
@pytest.fixture
def command() -> MyCommand:
    return MyCommand(settings=make_settings())

class TestMyCommand:
    def test_execute_succeeds(self, command): ...
```

## Release

Tag-based: push a git tag to trigger release workflow. No semantic-release.
