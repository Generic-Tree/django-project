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
SOURCE_DIR ?= $(ROOT_DIR)/src
VENV_DIR ?= $(ROOT_DIR)/venv
STATIC_DIR ?= $(SOURCE_DIR)/static
PROJECT_MODULE ?= src.__project__

# Target files
ENV_FILE ?= .env
REQUIREMENTS_TXT ?= requirements.txt
MANAGE_PY ?= $(SOURCE_DIR)/manage.py
PID_FILE ?= .pid
EPHEMERAL_ARCHIVES ?= \
	$(STATIC_DIR) \
	$(SOURCE_DIR)/db.sqlite3 \
	$(PID_FILE)

# Executables definition
DJANGO_ADMIN ?= $(PYTHON) $(MANAGE_PY)
PYTHON ?= $(VENV_DIR)/bin/python3
PIP ?= $(PYTHON) -m pip
GUNICORN ?= $(PYTHON) -m gunicorn


%: # Treat unrecognized targets
	@ printf "\033[31;1mUnrecognized routine: '$(*)'\033[0m\n"
	$(MAKE) help

help:: ## Show this help
	@ printf "\033[33;1mGNU-Make available routines:\n"
	egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[37;1m%-20s\033[0m %s\n", $$1, $$2}'

prepare:: ## Inicialize virtual environment
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	test -r $(ENV_FILE) || cp $(ENV_FILE).example $(ENV_FILE)

init:: veryclean prepare $(REQUIREMENTS_TXT) ## Configure development environment
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQUIREMENTS_TXT) --upgrade

execute:: setup run ## Setup and run application

setup:: clean compile ## Process source code into an executable program
	$(DJANGO_ADMIN) makemigrations
	$(DJANGO_ADMIN) migrate

compile:: ## Treat file generation
	$(DJANGO_ADMIN) collectstatic --noinput --clear --link

run:: ## Launch application locally
	$(GUNICORN) \
		--pid $(PID_FILE) \
		--pythonpath $(SOURCE_DIR) \
		--config python:$(PROJECT_MODULE).gunicorn \
		$(PROJECT_MODULE).wsgi

finish:: ## Stop application execution
	-test -r $(PID_FILE) && pkill --echo --pidfile $(PID_FILE)

check:: ## Output application status
	$(DJANGO_ADMIN) check
	$(DJANGO_ADMIN) diffsettings

clean:: ## Delete project ephemeral archives
	-rm -fr $(EPHEMERAL_ARCHIVES)

veryclean:: clean ## Delete all generated files
	-rm -fr $(VENV_DIR)
	find . -iname "*.pyc" -iname "*.pyo" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +


.EXPORT_ALL_VARIABLES:
.ONESHELL:
.PHONY: help prepare init execute setup compile run finish check clean veryclean
