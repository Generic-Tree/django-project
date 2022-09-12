# Development management facilities
#
# This file specifies useful routines to streamline development management.
# See https://www.gnu.org/software/make/.


# Tool configuration
SHELL := /bin/bash
GNUMAKEFLAGS += --no-print-directory

# Path record
ROOT_DIR ?= $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# Target files
REQUIREMENTS_TXT ?= requirements.txt
MANAGE_PY ?= manage.py
EPHEMERAL_ARCHIVES ?= \
	db.sqlite3

# Executables definition
PYTHON ?= $(VENV_DIR)/bin/python3
PIP ?= $(PYTHON) -m pip
DJANGO_ADMIN ?= $(PYTHON) $(MANAGE_PY)

# Execution configuration
VENV_DIR ?= venv
DJANGO_SETTINGS_MODULE ?= __project__.settings


%: # Treat unrecognized targets
	@ printf "\033[31;1mUnrecognized routine: '$(*)'\033[0m\n"
	$(MAKE) help

help:: ## Show this help
	@ printf "\033[33;1mGNU-Make available routines:\n"
	egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[37;1m%-20s\033[0m %s\n", $$1, $$2}'

prepare:: ## Inicialize virtual environment
	test -z $(VENV_DIR) -o -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)

init:: veryclean prepare $(REQUIREMENTS_TXT) ## Configure development environment
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS_TXT) --upgrade

execute:: setup run ## Setup and run application

setup:: clean ## Process source code into an executable program
	$(DJANGO_ADMIN) makemigrations
	$(DJANGO_ADMIN) migrate

run:: ## Launch application locally
	$(DJANGO_ADMIN) runserver

clean:: ## Delete project ephemeral archives
	-rm -fr $(EPHEMERAL_ARCHIVES)

veryclean:: clean ## Delete all generated files
	-rm -fr $(VENV_DIR)
	find . -iname "*.pyc" -iname "*.pyo" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +


.EXPORT_ALL_VARIABLES:
.ONESHELL:
.PHONY: help prepare init execute setup run clean veryclean
