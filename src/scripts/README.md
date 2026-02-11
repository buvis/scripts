Meta-package that installs all BUVIS CLI tools.

## Install

```bash
uv tool install buvis-scripts
```

## Update

```bash
uv tool upgrade buvis-scripts
```

Each release pins exact sub-package versions, so upgrades always get a coherent set.

## Individual tools

Install or upgrade a single tool instead:

```bash
uv tool install buvis-readerctl
uv tool upgrade buvis-readerctl
```

Available: `buvis-bim`, `buvis-dot`, `buvis-fctracker`, `buvis-hello-world`, `buvis-muc`, `buvis-outlookctl`, `buvis-pinger`, `buvis-readerctl`, `buvis-zseq`.
