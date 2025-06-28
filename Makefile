# Burnout Testing Framework Makefile

.PHONY: help install test test-cov lint format clean example

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	uv sync

test:  ## Run tests
	pytest

test-cov:  ## Run tests with coverage
	pytest --cov=burnout --cov-report=html --cov-report=term

test-fast:  ## Run only fast tests
	pytest -m "not slow"

lint:  ## Run linting
	ruff check .

format:  ## Format code
	ruff format .

clean:  ## Clean up generated files
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -f example_test_results.json

example:  ## Run example script
	python examples/simple_test_example.py

dev:  ## Install dev dependencies and setup pre-commit
	uv sync --group dev
	pre-commit install

# Install production dependencies
install-prod:
	uv sync

# Install development dependencies
install-dev:
	uv sync --dev
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
format-all: format-python format-mojo

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
	rm -rf htmlcov
	rm -rf .coverage
	rm -f example_test_results.json

# Development setup
setup: install-dev

# Add a new dependency
add:
	@read -p "Enter package name: " package; \
	uv add $$package

# Add a new development dependency
add-dev:
	@read -p "Enter package name: " package; \
	uv add --dev $$package

# Install modular nightly package
install-modular:
	uv pip install modular \
		--extra-index-url https://download.pytorch.org/whl/cpu \
		--index-url https://dl.modular.com/public/nightly/python/simple/ \
		--index-strategy unsafe-best-match 