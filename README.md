# Bob's Universal and Very Intelligent System scripts

This repository contains the scripts used by Bob's Universal and Very Intelligent System.

Feel free to reuse anything, but proceed with caution.

If you find something I could be doing a better way, please drop me an email at <tomas@buvis.net>.
I always appreciate any opportunity to learn. Thank you!

## Prerequisites

1. python
2. uv

## Install

No installation is required. The scripts are self-bootstrapping using `uv`.
Just make sure `uv` is installed and available in your PATH.

## Update

This can be automated if you create a post-merge hook (assuming scripts are cloned to home directory):

### Linux/macOS

1. Create `post-merge` in `.git/hooks`

    ```bash
    #!/bin/bash

    cd ~/scripts
    echo "Updating scripts"
    uv run --reinstall-package buvis-pybase --script bin/update-scripts
    cd -
    ```

2. Make it executable: `chmod +x .git/hooks/post-merge`

### Windows

1. Create `post-merge` in `.git/hooks`

    ```sh
    #!/bin/sh
    exec powershell.exe -ExecutionPolicy Bypass -File "$(dirname "$0")/post-merge.ps1"
    ```

2. Create `post-merge.ps1` in `.git/hooks`

    ```powershell
    $originalLocation = Get-Location
    Set-Location $env:USERPROFILE\scripts
    Write-Host "Updating scripts"
    uv run --reinstall-package buvis-pybase --script bin/update-scripts
    Set-Location $originalLocation
    ```

## Use

Anything in `./bin` folder can be executed and ideally provides usage instructions. It is a good idea to add the `bin` folder to your system path to make the scripts available anywhere.

The scripts use [PEP 723](https://peps.python.org/pep-0723/) inline metadata to declare their dependencies.
When you run a script, `uv` will automatically create an isolated environment and install the required dependencies (including `buvis-pybase`) if they are missing.

## Develop

### Activate virtual environment

You can use `uv` to create and manage virtual environments if needed, but for running scripts, `uv run` handles it automatically.

### Update python version

`uv` manages Python versions automatically. You can specify the version in `.python-version` or via `uv python install`.

### Concurrent development of prerequisite projects

The scripts are using `buvis-pybase`, `doogat-core` and `doogat-integrations` which I'm also developing.

To work with local versions, run `start-dev`.

To switch back to released versions, run `finish-dev`.

### Testing pre-release versions from test.pypi.org

To test a dev version of `buvis-pybase` published to test.pypi.org, update `pyproject.toml`:

```toml
dependencies = ["buvis-pybase==0.6.0.dev0"]  # pin to dev version

[[tool.uv.index]]
name = "testpypi"
url = "https://test.pypi.org/simple/"
explicit = true

[tool.uv.sources]
buvis-pybase = { index = "testpypi" }
```

To switch back to production, remove `[[tool.uv.index]]` and `[tool.uv.sources]` sections and use normal version spec.

Run `uv sync` after switching.
