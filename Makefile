# Burnout Testing Framework Makefile

.PHONY: help install test test-cov lint format clean example

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pixi install

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage
	pytest --cov=burnout --cov-report=html --cov-report=term

test-fast:  ## Run only fast tests
	pytest -m "not slow"

lint:  ## Run linting
	ruff check .
	ruff check --fix .

format:  ## Format code
	ruff format .
	black .
	isort .

clean:  ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf build/
	rm -rf dist/
	rm -rf .uv/
	rm -rf .pixi/
	rm -f example_test_results.json

example:  ## Run example script
	python examples/simple_test_example.py

dev:  ## Install dev dependencies and setup pre-commit
	pixi install --dev
	pre-commit install

# Install production dependencies
install-prod:
	pixi install

# Install development dependencies
install-dev:
	pixi install --dev
	pre-commit install

# Format code (Python)
format-python:
	ruff format .
	black .
	isort .

# Format Mojo code
format-mojo:
	mojo format .

# Format all code (Python + Mojo)
format-all: format format-mojo

# Type checking
type-check:
	mypy .

# Run all checks
check: format-all lint type-check

# Clean up
clean-all:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf build/
	rm -rf dist/
	rm -rf .uv/
	rm -rf .pixi/
	rm -f example_test_results.json

# Development setup
setup: install-dev

# Add a new dependency
add:
	@read -p "Enter package name: " package; \
	pixi add $$package

# Add a new development dependency
add-dev:
	@read -p "Enter package name: " package; \
	pixi add --dev $$package

# Install modular nightly package
install-modular:
	pixi add modular --channel modular-nightly

# Run pixi tasks
pixi-install:
	pixi run install

pixi-install-dev:
	pixi run install-dev

pixi-format:
	pixi run format

pixi-format-mojo:
	pixi run format-mojo

pixi-format-all:
	pixi run format-all

pixi-lint:
	pixi run lint

pixi-type-check:
	pixi run type-check

pixi-check:
	pixi run check

pixi-clean:
	pixi run clean

pixi-setup:
	pixi run setup 