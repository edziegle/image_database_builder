VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

venv:
	python3 -m venv $(VENV_NAME)

install-test: