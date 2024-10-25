.PHONY: install update run build clean

# https://stackoverflow.com/questions/18136918/how-to-get-current-relative-directory-of-your-makefile
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
parrent_name := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
parrent_path := $(patsubst %/,%,$(dir $(mkfile_path)))
NAME=$(subst -,_,$(parrent_name))

ifeq ($(OS),Windows_NT)
	SHELL := pwsh.exe
	.SHELLFLAGS := -NoProfile -Command
	CMD_RM := rm.ps1  # https://github.com/buvis/scripts/tree/main/bin
	CMD_MD := $$dir = md -Force
else
	CMD_RM := rm -rf
	CMD_MD := mkdir -p
endif

$(info Using $(SHELL) as shell)

install:
	poetry install

update:
	poetry update

run:
# if there is no lock then install dependencies
ifeq ("$(wildcard $(parrent_path)/poetry.lock)","")
	make install
endif
	poetry run python $(NAME)/cli.py $(ARGS)

clean:
	$(CMD_RM) $(NAME).build/
	$(CMD_RM) $(NAME).dist/
	$(CMD_RM) $(NAME).egg-info/
	$(CMD_RM) poetry.lock
	poetry env remove --all
ifeq ($(OS),Windows_NT)
	Get-ChildItem * -Include *.pyc -Recurse | Remove-Item
	Get-ChildItem * -Include *.pyo -Recurse | Remove-Item
	Get-ChildItem * -Include *~ -Recurse | Remove-Item
else
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
endif
