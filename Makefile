VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

.PHONY: venv install-test install-dev install test clean

clean:
	rm -rf logs

venv:
	python3 -m venv $(VENV_NAME)

install-test: requirements-test.txt
	pip install -r requirements-test.txt

install-dev: requirements.txt
	pip install -r requirements.txt

install: install-dev install-test

test: install-test
	python -m pytest