# Steno™ - AI Chat Recorder
#
# MIT License
#
# Copyright © 2024 Joshua M. Dotson (contact@cryorithm.org)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


.PHONY: all $(shell grep '^[^#[:space:]].*:' Makefile | sed 's/:.*//')

PKG ?= pytest

help:
	@echo "Usage: make <target>"
	@echo "  help                 Show this help message"
	@echo "  add                  Add a runtime package using Poetry (set $$PKG)"
	@echo "  add-dev              Add a development package using Poetry (set $$PKG)"
	@echo "  build                Build the package using Poetry"
	@echo "  check                Perform all checks (linting, testing, and poetry integrity)"
	@echo "  check-poetry         Run 'poetry check'"
	@echo "  install              Reinstall the project requirements"
	@echo "  install-poetry       Reinstall the Poetry dependencies in sync mode"
	@echo "  install-precommit    Run 'pre-commit {clean,install}'"
	@echo "  lint                 Run 'pre-commit run all files'"
	@echo "  run                  Run a custom script 'my-script' within the Poetry environment"
	@echo "  shell                Start a shell within the Poetry virtual environment"
	@echo "  show                 Show all packages installed via Poetry"
	@echo "  test                 Run pytest within the Poetry environment"
	@echo "  update               Run 'poetry update' to update dependencies"
	@echo "  update-poetry        Update Poetry to the latest version"
	@echo "  update-requirements  Update the requirements.txt file"

add:
	poetry add $(PKG)

add-dev:
	poetry add $(PKG) --dev --group dev

build:
	poetry build

check: lint test check-poetry

check-poetry:
	poetry check

install:
	poetry install

install-poetry:
	poetry self install --sync

install-precommit:
	pre-commit clean
	pre-commit install

lint:
	poetry run pre-commit run --all-files

run: install update
	poetry run steno

shell:
	poetry shell

show:
	poetry show

test:
	poetry run pytest

update:
	poetry update

update-poetry:
	poetry self update

update-requirements:
	poetry run python ./helpers/update_requirements.py
