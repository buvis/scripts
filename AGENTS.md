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
├── scripts/            # Meta-package (installs all tools)
└── zseq/               # Zettelsequence utilities
dev/
├── devmode.py          # Toggle local dependency mode
├── deps.toml           # Local dependency mappings
├── pin_deps.py         # Pin/unpin deps from uv.lock
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

## Installation (end users)

```bash
uv tool install buvis-scripts              # all tools
uv tool install buvis-readerctl            # single tool
```

Update:
```bash
uv tool upgrade buvis-scripts              # all tools (pinned coherent set)
uv tool upgrade buvis-readerctl            # single tool
```

The meta-package (`buvis-scripts`) pins exact sub-package versions, so upgrading it always gets a coherent set released together.

## Release

Tag-based via `bin/release`. CI pins deps before publishing to PyPI.

```bash
bin/release <pkg> patch|minor|major     # individual package
bin/release bundle patch|minor|major    # meta-package (buvis-scripts)
```

Typical flow: release individual packages first, then `bin/release bundle patch` to publish a `buvis-scripts` that pins those versions.

**What `bin/release` does** (individual):
1. Bumps version in `pyproject.toml` + `__init__.py`
2. Runs `uv lock`
3. Commits, tags `<pkg>-v<new>`, pushes

**Bundle release** updates `src/scripts/pyproject.toml` deps to match current package versions, then bumps + tags.

**CI publish workflow** (`.github/workflows/publish.yml`):
- Triggers on `*-v*` tags or manual dispatch
- Runs `dev/pin_deps.py` to rewrite range deps to exact pins before build
- Publishes wheel to PyPI with trusted publishing

**Dep pinning** (`dev/pin_deps.py`):
```bash
python dev/pin_deps.py src/readerctl          # pin from uv.lock
python dev/pin_deps.py src/readerctl --unpin  # restore ranges
```
