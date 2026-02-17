# AGENTS.md

BUVIS scripts repo. Standalone scripts in `bin/`, run via `uv run --script`.

## Structure

```text
bin/            # Standalone scripts (bash, python w/ PEP 723 inline metadata)
test-area/      # Gitignored scratch space
```

## Conventions

- Scripts use PEP 723 inline metadata for Python dependencies
- `uv run --script bin/<name>` handles isolated envs automatically
- Bash scripts use `set -euC`
- Add `bin/` to PATH for global access
