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
REPO_DIR ?= $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SOURCE_DIR ?= src
BACKEND_DIR ?= $(SOURCE_DIR)/service
VENV_DIR ?= venv

# Target files
ENV_FILE ?= .env
REQUIREMENTS_TXT ?= requirements.txt
EPHEMERAL_ARCHIVES ?= \
	src/service/static \
	src/service/db.sqlite3

# Executables definition
DJANGO_ADMIN ?= $(PYTHON) $(BACKEND_DIR)/manage.py
PYTHON ?= $(VENV_DIR)/bin/python3
PIP ?= $(PYTHON) -m pip
REMOVE ?= rm -fr


%: # Treat unrecognized targets
	@ printf "\033[31;1mUnrecognized routine: '$(*)'\033[0m\n"
	$(MAKE) help

help:: ## Show this help
	@ printf "\033[33;1mGNU-Make available routines:\n"
	egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[37;1m%-20s\033[0m %s\n", $$1, $$2}'

prepare:: ## Inicialize virtual environment
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	test -d $(ENV_FILE) || cp .env.example $(ENV_FILE)

init:: veryclean $(REQUIREMENTS_TXT) ## Configure development environment
	$(MAKE) prepare
	$(PIP) install -r $(REQUIREMENTS_TXT) --upgrade

execute:: build run ## Build and Run application

build:: clean ## Process source code into an executable program
	$(DJANGO_ADMIN) makemigrations
	$(DJANGO_ADMIN) migrate
	$(DJANGO_ADMIN) makemessages --all --ignore $(VENV_DIR)

compile:: ## Treat file generation
	$(DJANGO_ADMIN) collectstatic --noinput
	$(DJANGO_ADMIN) compilemessages

run:: ## Launch application locally
	$(DJANGO_ADMIN) runserver

check:: ## Output application status
	$(DJANGO_ADMIN) check
	$(DJANGO_ADMIN) diffsettings --default __project__

test:: ## Verify application's behavior requirements completeness
	$(DJANGO_ADMIN) test

deploy:: build ## Deploy application

publish:: build ## Upload application container to registry

clean:: ## Delete project ephemeral archives
	rm -fr $(EPHEMERAL_ARCHIVES)

veryclean:: clean ## Delete all generated files
	$(REMOVE) $(VENV_DIR)
	find $(SOURCE_DIR) -iname "*.pyc" -iname "*.pyo" -delete
	find $(SOURCE_DIR) -name "__pycache__" -type d -exec rm -rf {} +


.EXPORT_ALL_VARIABLES:
.ONESHELL:
.PHONY: help prepare init execute build compile run test deploy publish clean veryclean
