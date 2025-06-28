"""Burnout: Pytest framework for testing PyTorch models against MAX graphs."""

__version__ = "0.1.0"

from .core import MAXGraphTester, ModelTester
from .utils import compare_outputs, generate_test_data

__all__ = [
    "ModelTester",
    "MAXGraphTester",
    "generate_test_data",
    "compare_outputs",
]
