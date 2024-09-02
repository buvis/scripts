# Bob's Universal and Very Intelligent System scripts

This repository contains the scripts used by Bob's Universal and Very Intelligent System.

Feel free to reuse anything, but proceed with caution.

If you find something I could be doing a better way, please drop me an email at tomas@buvis.net.
I always appreciate any opportunity to learn. Thank you!

## Prerequisites

1. python
2. poetry

## Install

Run the command below from repository's root directory to install the dependencies required by scripts runner and scripts that aren't using poetry managed virtual environments (yet).

```bash
poetry lock
poetry config virtualenvs.create false
poetry install --without dev
poetry config virtualenvs.create true
```

## Update

This can be automated if you create a post-checkout hook:

1. Create `post-merge` in `.git/hooks`

```bash
#!/bin/bash

cd ~/scripts
echo "Running poetry lock in ~/scripts"
poetry lock
echo "Installing dependencies system-wide"
poetry config virtualenvs.create false
poetry install --without dev
poetry config virtualenvs.create true
cd -
```

2. Make it executable: `chmod +x .git/hooks/post-merge`

## Use

Anything in `./bin` folder can be executed and ideally provides usage instructions. It is a good idea to add the `bin` folder to your system path to make the scripts available anywhere.

## Develop

### Activate virtual environment

```bash
poetry shell
```

It used to be done automatically by direnv, but in some cases I needed to work with system python inside this repository, so I'm rather activating it on demand.

### Add new dependencies

If these are specific to a script, then use poetry within script's source directory to manage that.

If these are BUVIS-wide, then:

1. Add it to `src/buvis`: `cd src/buvis; poetry add <package_name>; cd -`
2. Install for as runtime dependency in repository root: `poetry install <dependency>`

### Update dependencies

```bash
poetry update
```

### Update python version

1. Make sure to exit virtual environment launched by `poetry shell` previously
2. Point poetry to python you want to use: `poetry env use /usr/bin/python3`; alternatively, you can use asdf to set local python version
3. Refresh the environment: `poetry env remove --all; poetry install; poetry shell`

### Concurrent development of prerequisite projects

The scripts are using `doogat-core` which I'm also developing. Unfortunately, there is currently no easy way to use editable and non-editable packages in same `pyproject.toml` (see: https://github.com/python-poetry/poetry/issues/8219). So I need to modify `pyproject.toml`.

1. Uncomment `# doogat-core = {path = "../../doogat/doogat-core", develop = true}` in `pyproject.toml`
2. Update dependencies: `poetry update`
3. Do the work in both projects
4. When done, you push to `doogat-core` project first
5. Comment the line uncommented in step 1, and uncomment: `# doogat-core = {version = "*", source = "test-pypi"}`
6. Update dependencies: `poetry update`
7. Verify everything still works
8. Create release of `doogat-core`
9. Comment the line uncommented in step 5, and uncomment: `# doogat-core = "*"`
10. Now you can push the changes in this repository
