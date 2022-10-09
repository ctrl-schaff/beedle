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

# Virtual Environment
PY = python3
BIN = bin

# Requirements
REQ_DIR = req
REQ=$(REQ_DIR)/requirements.txt

all: install lint test

.PHONY: install
install:
> $(BIN)/pip install --upgrade -r $(REQ)

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
> $(BIN)/pylint --exit-zero ./z2p/*.py
> $(BIN)/flake8 --exit-zero --show-source ./z2p/*.py
> $(BIN)/pylint --exit-zero ./test/*.py
> $(BIN)/flake8 --exit-zero --show-source ./test/*.py

.PHONY: clean
clean:
> find . -type f -name *.pyc -delete
> find . -type d -name __pycache__ -delete
