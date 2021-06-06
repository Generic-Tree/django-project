SHELL := /bin/bash

BACKEND_ROOT ?= $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

VENV_ROOT ?= venv
PYTHON ?= $(VENV_ROOT)/bin/python3
DJANGO_ADMIN ?= $(PYTHON) $(BACKEND_ROOT)/manage.py


init:: veryclean requirements.txt isolate
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip freeze

isolate::
	test -d $(VENV_ROOT) || python3.9 -m venv $(VENV_ROOT)

execute:: build run

run::
	$(DJANGO_ADMIN) runserver

build:: compile
	$(DJANGO_ADMIN) makemigrations
	$(DJANGO_ADMIN) migrate

compile::
	$(DJANGO_ADMIN) collectstatic --noinput

test::
	$(DJANGO_ADMIN) test

clean::
	rm -fr static
	rm -fr db.sqlite3

veryclean:: clean
	rm -fr venv
	find -iname "*.pyc" -iname "*.pyo" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +


.ONESHELL:
.PHONY: init isolate execute run build compile test clean veryclean
