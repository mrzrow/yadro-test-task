VENV_DIR = .venv
PYTHON = python3
PIP = $(VENV_DIR)/bin/pip
APP = src.main:app
UVICORN = $(VENV_DIR)/bin/uvicorn
HOST = 0.0.0.0
PORT = 8000


.PHONY: install
install:
	$(PYTHON) -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt


.PHONY: run
run: 
	$(UVICORN) $(APP) --host $(HOST) --port $(PORT)
