"""Integration tests for the burnout framework."""

import pytest
import torch

from burnout.core import ModelTester
from burnout.utils import compare_outputs, create_simple_model, generate_test_data


class TestPyTorchMAXIntegration:
    """Integration tests for PyTorch and MAX comparison."""

    def setup_method(self):
        """Setup test method."""
        self.model = create_simple_model(10, 5)
        self.pytorch_tester = ModelTester(self.model)
        self.test_input = generate_test_data((1, 10), random_seed=42)

    def test_pytorch_inference_workflow(self):
        """Test complete PyTorch inference workflow."""
        # Run inference
        output = self.pytorch_tester.run_inference(self.test_input)

        # Verify output
        assert isinstance(output, torch.Tensor)
        assert output.shape == (1, 5)
        assert not torch.isnan(output).any()
        assert not torch.isinf(output).any()

    def test_benchmark_workflow(self):
        """Test complete benchmarking workflow."""
        # Run benchmark
        benchmark_results = self.pytorch_tester.benchmark(self.test_input, num_runs=5)

        # Verify results
        required_keys = [
            "mean_time_ms",
            "std_time_ms",
            "min_time_ms",
            "max_time_ms",
        ]
        for key in required_keys:
            assert key in benchmark_results
            assert benchmark_results[key] >= 0

        # Verify logical consistency
        assert benchmark_results["min_time_ms"] <= benchmark_results["mean_time_ms"]
        assert benchmark_results["mean_time_ms"] <= benchmark_results["max_time_ms"]

    @pytest.mark.skip(reason="MAX graph implementation not yet available")
    def test_pytorch_max_comparison(self):
        """Test comparison between PyTorch and MAX outputs."""
        # This test will be enabled once MAX graph implementation is available
        pytorch_output = self.pytorch_tester.run_inference(self.test_input)

        # Mock MAX output for now
        max_output = pytorch_output.detach().cpu().numpy()

        # Compare outputs
        comparison = compare_outputs(pytorch_output, max_output)

        assert comparison["passed"] is True
        assert comparison["max_abs_diff"] == 0.0


class TestDataGeneration:
    """Test data generation and consistency."""

    def test_deterministic_data_generation(self):
        """Test that data generation is deterministic with same seed."""
        data1 = generate_test_data((2, 3), random_seed=123)
        data2 = generate_test_data((2, 3), random_seed=123)

        assert torch.allclose(data1, data2)

    def test_different_seeds_produce_different_data(self):
        """Test that different seeds produce different data."""
        data1 = generate_test_data((2, 3), random_seed=123)
        data2 = generate_test_data((2, 3), random_seed=456)

        assert not torch.allclose(data1, data2)

    def test_data_statistics(self):
        """Test that generated data has reasonable statistics."""
        data = generate_test_data((1000, 10), random_seed=42)

        # Check mean is close to 0
        assert abs(data.mean().item()) < 0.1

        # Check std is close to 1
        assert abs(data.std().item() - 1.0) < 0.1
