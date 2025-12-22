# Bob's Universal and Very Intelligent System scripts

This repository contains the scripts used by Bob's Universal and Very Intelligent System.

Feel free to reuse anything, but proceed with caution.

If you find something I could be doing a better way, please drop me an email at <tomas@buvis.net>.
I always appreciate any opportunity to learn. Thank you!

## Prerequisites

1. python
2. poetry

## Install

Run the command below from repository's root directory to install the dependencies required by scripts runner and scripts that aren't using poetry managed virtual environments (yet).

```bash
poetry lock
poetry config virtualenvs.create false
poetry install --without dev,docs,test
poetry config virtualenvs.create true
```

## Update

This can be automated if you create a post-merge hook:

### Linux/macOS

1. Create `post-merge` in `.git/hooks`

    ```bash
    #!/bin/bash

    cd ~/scripts
    echo "Cleaning virtualenvs"
    poetry env remove --all
    echo "Switching to system-wide operations"
    poetry config virtualenvs.create false
    echo "Cleaning development cache"
    poetry cache clear test-pypi --all -q
    echo "Running poetry lock in ~/scripts"
    rm poetry.lock
    poetry lock
    echo "Installing dependencies"
    poetry install --without dev,docs,test
    echo "Switching to project-specific operations"
    poetry config virtualenvs.create true
    echo "Updating scripts dependencies"
    update-scripts-dependencies
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
    Write-Host "Cleaning development cache"
    poetry cache clear test-pypi --all -q
    Write-Host "Running poetry lock"
    Remove-Item poetry.lock -ErrorAction SilentlyContinue
    poetry lock
    Write-Host "Installing dependencies"
    poetry install --without dev,docs,test
    Write-Host "Updating scripts dependencies"
    poetry run python bin/update-scripts-dependencies
    Set-Location $originalLocation
    ```

## Use

Anything in `./bin` folder can be executed and ideally provides usage instructions. It is a good idea to add the `bin` folder to your system path to make the scripts available anywhere.

## Develop

### Activate virtual environment

```bash
poetry shell
```

It used to be done automatically by direnv, but in some cases I needed to work with system python inside this repository, so I'm rather activating it on demand.

### Update python version

1. Make sure to exit virtual environment launched by `poetry shell` previously
2. Install latest python available:
   - macOS: `asdf install python $(asdf latest python)`
   - Windows:
        1. Get available versions: `pyenv install -l`
        2. Install the latest one: `pyenv install X.Y.Z`
3. Point poetry to python you want to use: `poetry env use /usr/bin/python3`; alternatively, you can use asdf to set local python version
4. Refresh the environment: `poetry env remove --all; poetry install; poetry shell`

### Concurrent development of prerequisite projects

The scripts are using `buvis-pybase` and `doogat-core` which I'm also developing. Unfortunately, there is currently no easy way to use editable and non-editable packages in same `pyproject.toml` (see: <https://github.com/python-poetry/poetry/issues/8219>). So I need to modify `pyproject.toml`.

1. Switch to local files:
   - macOS: Uncomment `# buvis-pybase = {path = "../buvis-pybase", develop = true}` or `# doogat-core = {path = "../../doogat/doogat-core", develop = true}` in `pyproject.toml`
   - Windows (there is an issue in Poetry in Windows causing it to be unable to resolve pth files):
     - in scripts root: `pip install -e ../buvis-pybase/` or `pip install -e ..\..\doogat\doogat-core\`
     - in script's root (like `src/bim` for example): `pip install -e ../../../buvis-pybase/` or `pip install -e ..\..\..\..\doogat\doogat-core\`
2. Update dependencies: `poetry update`
3. Do the work in both projects
4. When done, you push to `buvis-pybase` project first
5. Comment out the line uncommented in step 1, and uncomment: `# buvis-pybase = {version = "*", source = "test-pypi"}`
6. Clear development cache: `poetry cache clear test-pypi --all`
7. Update dependencies: `poetry update`
8. Verify everything still works
9. Release `buvis-pybase`
10. Comment the line uncommented in step 5, update `<NEW_VERSION>` and uncomment: `# buvis-pybase = "<NEW_VERSION>"`
11. Now you can push the changes in this repository

### Run tests

While you are in `scripts` directory with `poetry shell` activated, run: `poetry run pytest src/<script_name>`.
