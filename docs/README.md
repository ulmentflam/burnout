# Burnout Testing Framework Documentation

## Overview

Burnout is a Pytest-based framework designed to test PyTorch models against MAX graphs. It provides automated testing, benchmarking, and comparison capabilities for validating model implementations across different execution environments.

## Architecture

### Core Components

1. **ModelTester**: Handles PyTorch model testing and benchmarking
2. **MAXGraphTester**: Handles MAX graph testing and benchmarking (placeholder for MAX SDK integration)
3. **TestSuite**: Abstract base class for creating custom test suites
4. **Utilities**: Helper functions for data generation, output comparison, and result management

### Project Structure

```
burnout/
├── burnout/
│   ├── __init__.py      # Package initialization
│   ├── core.py          # Core testing classes
│   └── utils.py         # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_core.py     # Core functionality tests
│   └── test_integration.py  # Integration tests
├── examples/
│   └── simple_test_example.py  # Usage example
└── docs/
    └── README.md        # This file
```

## Quick Start

### Installation

```bash
# Install dependencies
uv sync

# Run tests
pytest

# Run with coverage
pytest --cov=burnout
```

### Basic Usage

```python
import torch
from burnout.core import ModelTester
from burnout.utils import create_simple_model, generate_test_data

# Create a model
model = create_simple_model(input_size=10, output_size=5)
tester = ModelTester(model)

# Generate test data
test_input = generate_test_data((1, 10), random_seed=42)

# Run inference
output = tester.run_inference(test_input)

# Benchmark performance
results = tester.benchmark(test_input, num_runs=100)
print(f"Mean inference time: {results['mean_time_ms']:.2f} ms")
```

## Testing Features

### Model Testing

- **Inference Testing**: Run models with test data and validate outputs
- **Performance Benchmarking**: Measure inference time with statistical analysis
- **Memory Usage**: Track memory consumption during inference
- **Error Detection**: Identify NaN/Inf values in outputs

### Output Comparison

- **Accuracy Validation**: Compare PyTorch and MAX outputs with configurable tolerances
- **Shape Validation**: Ensure output shapes match between implementations
- **Statistical Analysis**: Calculate absolute and relative differences
- **Detailed Reporting**: Generate comprehensive comparison reports

### Data Generation

- **Deterministic Generation**: Reproducible test data with seed control
- **Flexible Shapes**: Support for arbitrary tensor shapes
- **Type Control**: Configurable data types (float32, float64, etc.)
- **Statistical Properties**: Generate data with specific distributions

## Configuration

### Pytest Configuration

The framework uses `pytest.ini` for configuration:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### Test Markers

- `@pytest.mark.slow`: Mark tests that take longer to run
- `@pytest.mark.integration`: Mark integration tests
- `@pytest.mark.unit`: Mark unit tests

## Extending the Framework

### Creating Custom Test Suites

```python
from burnout.core import TestSuite

class CustomTestSuite(TestSuite):
    def setup(self):
        # Initialize test environment
        pass
    
    def teardown(self):
        # Cleanup test environment
        pass
    
    def run_tests(self):
        # Run custom tests
        return {"results": "custom"}
```

### Adding MAX Graph Support

To integrate with MAX graphs, implement the placeholder methods in `MAXGraphTester`:

```python
def _load_graph(self):
    # Load MAX graph using MAX SDK
    pass

def run_inference(self, input_data):
    # Run inference on MAX graph
    pass

def benchmark(self, input_data, num_runs=100):
    # Benchmark MAX graph performance
    pass
```

## Best Practices

### Test Design

1. **Use Deterministic Data**: Always use fixed random seeds for reproducible tests
2. **Test Edge Cases**: Include tests for boundary conditions and error cases
3. **Performance Testing**: Run benchmarks with sufficient iterations for statistical significance
4. **Memory Management**: Clean up resources in test teardown

### Code Quality

1. **Type Hints**: Use comprehensive type annotations
2. **Documentation**: Document all public APIs and complex logic
3. **Error Handling**: Implement robust error handling and validation
4. **Testing**: Maintain high test coverage for all components

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `uv sync`
2. **CUDA Issues**: Check device availability for GPU testing
3. **Memory Issues**: Monitor memory usage during large model testing
4. **Performance Variability**: Use sufficient warmup runs before benchmarking

### Debug Mode

Enable debug output by setting environment variables:

```bash
export BURNOUT_DEBUG=1
pytest -v
```

## Contributing

1. Follow the established code style (Black + Ruff)
2. Add tests for new functionality
3. Update documentation for API changes
4. Use type hints and docstrings
5. Run the full test suite before submitting changes

## License

This project is part of the Modular Hack Weekend and follows the project's licensing terms.
