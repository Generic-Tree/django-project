# Development management facilities
#
# This file specifies useful routines to streamline development management.
# See https://www.gnu.org/software/make/.


# Consume environment variables
ifneq (,$(wildcard .env))
	include .env
endif

# Tool configuration
SHELL := /bin/bash
GNUMAKEFLAGS += --no-print-directory

# Path record
ROOT_DIR ?= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
VENV_DIR ?= $(ROOT_DIR)/venv

# Target files
ENV_FILE ?= .env
REQUIREMENTS_TXT ?= requirements.txt
MANAGE_PY ?= manage.py
EPHEMERAL_ARCHIVES ?= \
	db.sqlite3

# Behavior setup
PROJECT_NAME ?= $(shell basename $(ROOT_DIR) | tr a-z A-Z)

# Executables definition
GIT ?= git
DJANGO_ADMIN ?= $(PYTHON) $(MANAGE_PY)
PYTHON ?= $(VENV_DIR)/bin/python3
PIP ?= $(PYTHON) -m pip


%: # Treat unrecognized targets
	@ printf "\033[31;1mUnrecognized routine: '$(*)'\033[0m\n"
	$(MAKE) help

help:: ## Show this help
	@ printf "\033[33;1m$(PROJECT_NAME)'s GNU-Make available routines:\n"
	egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[37;1m%-20s\033[0m %s\n", $$1, $$2}'

prepare:: ## Inicialize virtual environment
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	test -r $(ENV_FILE) -o ! -r $(ENV_FILE).example || cp $(ENV_FILE).example $(ENV_FILE)

init:: veryclean prepare $(REQUIREMENTS_TXT) ## Configure development environment
	$(GIT) submodule update --init --recursive
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS_TXT) --upgrade

up:: build execute ## Build and execute service

build:: clean ## Build service running environment

execute:: setup run ## Setup and run application

setup:: clean compile ## Process source code into an executable program
	$(DJANGO_ADMIN) makemigrations
	$(DJANGO_ADMIN) migrate

compile:: ## Treat file generation

run:: ## Launch application locally
	$(DJANGO_ADMIN) runserver

finish:: ## Stop application execution

status:: ## Present service running status

ping:: ## Verify service reachability

test:: ## Verify application's behavior requirements completeness

release:: ## Release a new project version

publish:: ## Publish current project version

deploy:: ## Deploy service on remote server

clean:: ## Delete project ephemeral archives
	-rm --force --recursive $(EPHEMERAL_ARCHIVES)

veryclean:: clean ## Delete all generated files
	-rm --force --recursive $(VENV_DIR)
	find . -iname "*.pyc" -iname "*.pyo" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +


.EXPORT_ALL_VARIABLES:
.ONESHELL:
.PHONY: help prepare init up build execute setup compile run finish status ping test release publish deploy clean veryclean
