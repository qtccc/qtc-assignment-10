# Define variables
APP_NAME = app.py
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
FLASK_APP = $(APP_NAME)

# Default target
.PHONY: all
all: run

# Create a virtual environment
.PHONY: venv
venv:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip

# Install dependencies
.PHONY: install
install: venv
	$(PIP) install -r requirements.txt

# Run the Flask application
.PHONY: run
run:
	FLASK_APP=$(FLASK_APP) FLASK_ENV=development $(PYTHON) -m flask run

# Clean up temporary files
.PHONY: clean
clean:
	rm -rf __pycache__
	rm -rf $(VENV_DIR)
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Create requirements.txt
.PHONY: freeze
freeze:
	$(PIP) freeze > requirements.txt

# Lint the code using flake8 (optional)
.PHONY: lint
lint:
	$(PIP) install flake8
	$(VENV_DIR)/bin/flake8 --max-line-length=88 .