.PHONY: install update run build clean

# https://stackoverflow.com/questions/18136918/how-to-get-current-relative-directory-of-your-makefile
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
parrent_name := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
parrent_path := $(patsubst %/,%,$(dir $(mkfile_path)))
NAME=$(subst -,_,$(parrent_name))

ifeq ($(OS),Windows_NT)
	SHELL := pwsh.exe
	.SHELLFLAGS := -NoProfile -Command
	CMD_RM := .\rm.ps1
	CMD_MD := $$dir = md -Force
else
	CMD_RM := rm -rf
	CMD_MD := mkdir -p
endif

$(info Using $(SHELL) as shell)

install:
	$(CMD_RM) Pipfile.lock
	pipenv install --dev

update:
	pipenv update --dev

test:
ifeq ("$(wildcard $(parrent_path)/Pipfile.lock)","")
	make install
endif
	pipenv run pytest -v
