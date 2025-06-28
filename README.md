# Burnout

A PyTorch compilation library that targets MAX (Modular Accelerator eXchange) graphs for high-performance execution.

## Features

- **MAX Compilation Decorator**: Similar to `torch.compile`, but generates MAX graphs instead of TorchInductor code
- **Graph Tracing**: Advanced graph tracing and optimization capabilities
- **Multiple Compilation Modes**: Support for different optimization strategies
- **Caching**: Disk-based caching of compiled graphs for faster subsequent runs
- **Verbose Compilation**: Detailed compilation information and debugging
- **Automated Testing**: Framework for testing PyTorch models against MAX graph implementations
- **Performance Benchmarking**: Compare PyTorch and MAX performance
- **Accuracy Validation**: Validate outputs between PyTorch and MAX implementations

## Quick Start

```bash
# Install dependencies
uv sync

# Run tests
pytest

# Run with coverage
pytest --cov=burnout

# Run the example
python examples/compile_example.py
```

## Basic Usage

```python
import torch
from burnout import compile

@compile
def my_function(x, y):
    return torch.matmul(x, y) + torch.relu(x)

# Use with options
@compile(
    backend="max",
    mode="max-autotune",
    fullgraph=True
)
def optimized_function(x, y):
    return torch.matmul(x, y) + torch.relu(x)
```

## Verbose Compilation

```python
from burnout import compile_verbose

@compile_verbose(mode="max-autotune", verbose=True)
def verbose_function(x, y):
    return torch.matmul(x, y) + torch.relu(x)
```

## Cached Compilation

```python
from burnout import compile_with_cache

@compile_with_cache(cache_dir=".my_cache", mode="max-autotune")
def cached_function(x, y):
    return torch.matmul(x, y) + torch.relu(x)
```

## Examples

Run the comprehensive example:

```bash
python examples/compile_example.py
```

## Compilation Modes

- **`default`**: Basic optimization with operation fusion
- **`reduce-overhead`**: Focus on reducing compilation overhead
- **`max-autotune`**: Aggressive optimization with all available passes

## Project Structure

- `burnout/` - Core compilation framework
  - `compile.py` - MAX compilation decorators
  - `graph_tracer.py` - Graph tracing and optimization
  - `core.py` - Testing framework for PyTorch vs MAX
  - `utils.py` - Utility functions
- `tests/` - Test suites and examples
- `examples/` - Sample usage and demonstrations

## Architecture

The framework consists of several key components:

1. **MAX Compilation Decorator**: Main interface similar to `torch.compile`
2. **Graph Tracer**: Converts PyTorch functions to graph representations
3. **Graph Builder**: Manages the compilation pipeline and caching
4. **Graph Optimizer**: Applies various optimization passes
5. **MAX Graph Converter**: Transforms PyTorch FX graphs to MAX format

## Development

```bash
# Install development dependencies
uv sync --extra dev

# Run linting
ruff check .

# Run type checking
mypy burnout/

# Run tests
pytest tests/

# Run examples
python examples/compile_example.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
