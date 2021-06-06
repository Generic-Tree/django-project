SHELL := /bin/bash

REPO_ROOT ?= $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
BACKEND_ROOT ?= src

#include .env
include $(BACKEND_ROOT)/Makefile


help: ## Show this help
	@ egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[3	7;1m%-20s\033[0m %s\n", $$1, $$2}'

init:: veryclean | isolate ## Configure the development environment

isolate::  ## Guarantee environment isolation is set

execute:: build run ## Build and Run application

run:: ## Launch application locally

build:: ## Process source code into an executable program

compile:: ## Treat file generation

test:: ## Verify application's behavior requirements completeness

clean:: ## Delete all files created through Build process

veryclean:: clean ## Delete all generated files

deploy:: build ## Deploy application


.ONESHELL:
.PHONY: help init isolate execute run build compile test clean veryclean deploy