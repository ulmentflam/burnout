"""Utility functions for the burnout testing framework."""

from typing import Any, Optional

import numpy as np
import torch


def generate_test_data(
    shape: tuple[int, ...],
    dtype: torch.dtype = torch.float32,
    random_seed: Optional[int] = None,
) -> torch.Tensor:
    """Generate test data with specified shape and dtype."""
    if random_seed is not None:
        torch.manual_seed(random_seed)
        np.random.seed(random_seed)

    return torch.randn(shape, dtype=dtype)


def compare_outputs(
    pytorch_output: torch.Tensor,
    max_output: np.ndarray,
    tolerance: float = 1e-5,
    rtol: float = 1e-5,
    atol: float = 1e-8,
) -> dict[str, Any]:
    """Compare PyTorch and MAX outputs for accuracy."""
    # Convert PyTorch tensor to numpy for comparison
    pytorch_np = pytorch_output.detach().cpu().numpy()

    # Ensure shapes match
    if pytorch_np.shape != max_output.shape:
        return {
            "passed": False,
            "error": (
                f"Shape mismatch: PyTorch {pytorch_np.shape} vs MAX"
                f" {max_output.shape}"
            ),
        }

    # Calculate differences
    abs_diff = np.abs(pytorch_np - max_output)
    rel_diff = abs_diff / (np.abs(pytorch_np) + 1e-8)

    # Check tolerances
    passed = np.allclose(pytorch_np, max_output, rtol=rtol, atol=atol)

    return {
        "passed": bool(passed),
        "max_abs_diff": float(np.max(abs_diff)),
        "mean_abs_diff": float(np.mean(abs_diff)),
        "max_rel_diff": float(np.max(rel_diff)),
        "mean_rel_diff": float(np.mean(rel_diff)),
        "pytorch_shape": pytorch_np.shape,
        "max_shape": max_output.shape,
    }


def create_simple_model(input_size: int, output_size: int) -> torch.nn.Module:
    """Create a simple PyTorch model for testing."""
    return torch.nn.Sequential(
        torch.nn.Linear(input_size, 64),
        torch.nn.ReLU(),
        torch.nn.Linear(64, 32),
        torch.nn.ReLU(),
        torch.nn.Linear(32, output_size),
    )


def save_test_results(results: dict[str, Any], filename: str) -> None:
    """Save test results to a JSON file."""
    import json
    from datetime import datetime

    # Add timestamp
    results["timestamp"] = datetime.now().isoformat()

    with open(filename, "w") as f:
        json.dump(results, f, indent=2, default=str)
