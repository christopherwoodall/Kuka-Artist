# Define the Python files
PYTHON_FILES := $(wildcard src/*.py)

# Define the tools
FLAKE8 = flake8
MYPY = mypy
BLACK = black

# Default target
all: lint format

# Lint target
lint: flake8 mypy

flake8:
	$(FLAKE8) $(PYTHON_FILES)

mypy:
	$(MYPY) $(PYTHON_FILES)

# Format target
format: black

black:
	$(BLACK) $(PYTHON_FILES)

# Clean target (optional)
clean:
	@echo "Cleaning up..."

.PHONY: all lint format clean