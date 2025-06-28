"""Tests for core burnout functionality."""

import numpy as np
import torch

from burnout.core import ModelTester
from burnout.utils import compare_outputs, create_simple_model, generate_test_data


class TestModelTester:
    """Test the ModelTester class."""

    def setup_method(self):
        """Setup test method."""
        self.model = create_simple_model(10, 5)
        self.tester = ModelTester(self.model)
        self.test_input = generate_test_data((1, 10), random_seed=42)

    def test_model_tester_initialization(self):
        """Test ModelTester initialization."""
        assert self.tester.model is self.model
        assert self.tester.device == "cpu"
        assert self.tester.model.training is False

    def test_run_inference(self):
        """Test model inference."""
        output = self.tester.run_inference(self.test_input)
        assert isinstance(output, torch.Tensor)
        assert output.shape == (1, 5)

    def test_benchmark(self):
        """Test model benchmarking."""
        results = self.tester.benchmark(self.test_input, num_runs=10)

        assert "mean_time_ms" in results
        assert "std_time_ms" in results
        assert "min_time_ms" in results
        assert "max_time_ms" in results

        assert results["mean_time_ms"] > 0
        assert (
            results["min_time_ms"] <= results["mean_time_ms"] <= results["max_time_ms"]
        )


class TestUtils:
    """Test utility functions."""

    def test_generate_test_data(self):
        """Test test data generation."""
        data = generate_test_data((2, 3), random_seed=123)
        assert isinstance(data, torch.Tensor)
        assert data.shape == (2, 3)
        assert data.dtype == torch.float32

    def test_compare_outputs_matching(self):
        """Test output comparison with matching outputs."""
        pytorch_output = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
        max_output = np.array([[1.0, 2.0], [3.0, 4.0]])

        result = compare_outputs(pytorch_output, max_output)
        assert result["passed"] is True
        assert result["max_abs_diff"] == 0.0

    def test_compare_outputs_different(self):
        """Test output comparison with different outputs."""
        pytorch_output = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
        max_output = np.array([[1.1, 2.0], [3.0, 4.1]])

        result = compare_outputs(pytorch_output, max_output)
        assert result["passed"] is False
        assert result["max_abs_diff"] > 0.0

    def test_compare_outputs_shape_mismatch(self):
        """Test output comparison with shape mismatch."""
        pytorch_output = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
        max_output = np.array([[1.0, 2.0, 3.0]])

        result = compare_outputs(pytorch_output, max_output)
        assert result["passed"] is False
        assert "Shape mismatch" in result["error"]

    def test_create_simple_model(self):
        """Test simple model creation."""
        model = create_simple_model(10, 5)
        assert isinstance(model, torch.nn.Module)

        # Test forward pass
        input_tensor = torch.randn(1, 10)
        output = model(input_tensor)
        assert output.shape == (1, 5)
