VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

.PHONY: venv install-test install-dev install test clean upgrade-deps

clean: clean-database clean-logs

clean-logs: logs
	rm -rf logs/*

clean-database: image-database.db
	rm image-database.db

venv:
	python3 -m venv $(VENV_NAME)

install-test: requirements-test.txt
	pip install -r requirements-test.txt

install-dev: requirements.txt
	pip install -r requirements.txt

install: install-dev install-test

upgrade-deps: requirements.txt requirements-test.txt
	pip install -r requirements.txt --upgrade
	pip install -r requirements-test.txt --upgrade

test: install-test
	python -m pytest

run-sample: clean
	python src/builder.py bin/sampleindex