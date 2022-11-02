SHELL := bash

.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c 
.DELETE_ON_ERROR:

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

ifeq ($(origin .RECIPEPREFIX), undefined)
	$(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >

# Directory Structure
PROJECT_NAME = beedle
REQUIREMENTS = requirements.txt
TEST_DIRECTORY = test


# Virtual Environment
PY = python3
BIN = bin

# Requirements
REQ_DIR = req

all: install lint test

.PHONY: install
install:
> $(BIN)/pip install -I -r $(REQUIREMENTS)

.PHONY: localbuild
localbuild:
> $(PY) setup.py build_ext --inplace 

.PHONY: test
test: 
> $(PY) -m pytest

.PHONY: collect_tests
collect_tests: 
> $(PY) -m pytest --collect-only

.PHONY: lint 
lint: 
> $(BIN)/pylint --exit-zero --jobs 0 --recursive true $(PROJECT_NAME)
> $(BIN)/flake8 --exit-zero --show-source --statistics --benchmark $(PROJECT_NAME)
> $(BIN)/pylint --exit-zero --jobs 0 --recursive true $(TEST_DIRECTORY)
> $(BIN)/flake8 --exit-zero --show-source --statistics --benchmark $(TEST_DIRECTORY)

.PHONY: clean
clean:
> find . -type f -name *.pyc -delete
> find . -type d -name __pycache__ -delete
