
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

.PHONY: debugtest
debugtest: 
> $(PY) -m pytest --pdb -s

.PHONY: lint 
lint: 
> $(BIN)/flake8 z2p

.PHONY: clean
clean:
> find . -type f -name *.pyc -delete
> find . -type d -name __pycache__ -delete
