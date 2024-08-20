# Bob's Universal and Very Intelligent System scripts

This repository contains the scripts used by Bob's Universal and Very Intelligent System.

Feel free to reuse anything, but proceed with caution.

If you find something I could be doing a better way, please drop me an email at tomas@buvis.net.
I always appreciate any opportunity to learn. Thank you!

## Install

Run the command below from repository's root directory to install the dependencies required by scripts runner and scripts that aren't using poetry managed virtual environments (yet).

```bash
pipenv lock
pipenv install --system
```

## Update

This can be automated if you create a post-checkout hook:

1. Create `post-checkout` in `.git/hooks`

```bash
#!/bin/bash
# Post-checkout hook to run pipenv lock and pipenv install --system

# Fetch the flag indicating whether it was a branch checkout (1) or not (0)
CHECKOUT_TYPE=$3

# Only run pipenv commands if it was a branch checkout
if [ "$CHECKOUT_TYPE" -eq 1 ]; then
    echo "Running pipenv lock..."
    cd scripts && pipenv lock
    echo "Installing dependencies system-wide..."
    cd scripts && pipenv install --system
fi
```

2. Make it executable: `chmod +x .git/hooks/post-checkout`

## Develop

### Activate virtual environment

```bash
pipenv shell
```

It was done automatically by direnv, but in some cases I needed to work with system python inside this repository, so I'm rather activating it on demand.

### Add new dependencies

If these are specific to a script, then use poetry within script's source directory to manage that.

If these are BUVIS-wide, then:

1. Add it to `src/buvis/setup.py` in `dependencies` list
2. Install for as runtime dependency in repository root: `pipenv install <dependency>`
3. Add it to `~/.default-python-packages` (if using `buvis/home` dotfiles)

### Update dependencies

```bash
pipenv update
```

### Update python version

Replace `xx.y` below by target version you want to use. Make sure you exited `pipenv shell` before running the command.

```bash
export PYTHON_VERSION=3.xx.y
pipenv --rm; pipenv install --dev --python $PYTHON_VERSION; pipenv shell
```
