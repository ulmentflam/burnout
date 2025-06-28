# burnout

A Pytest framework for testing PyTorch models against MAX graphs during Modular Hack Weekend.

## Features

- Automated testing of PyTorch models against MAX graph implementations
- Performance benchmarking and comparison
- Accuracy validation between PyTorch and MAX outputs
- Configurable test suites for different model architectures

## Quick Start

```bash
# Install dependencies
uv sync

# Run tests
pytest

# Run with coverage
pytest --cov=burnout
```

## Project Structure

- `burnout/` - Core testing framework
- `tests/` - Test suites and examples
- `examples/` - Sample PyTorch models and MAX graphs
