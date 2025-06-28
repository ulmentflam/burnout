#!/usr/bin/env python3
"""Example usage of the burnout testing framework."""

from burnout.core import ModelTester
from burnout.utils import (
    compare_outputs,
    create_simple_model,
    generate_test_data,
    save_test_results,
)


def main():
    """Run a simple example test."""
    print("🔥 Burnout Testing Framework Example")
    print("=" * 50)

    # Create a simple PyTorch model
    print("1. Creating PyTorch model...")
    model = create_simple_model(input_size=10, output_size=5)

    # Create test data
    print("2. Generating test data...")
    test_input = generate_test_data((1, 10), random_seed=42)

    # Initialize tester
    print("3. Initializing ModelTester...")
    tester = ModelTester(model)

    # Run inference
    print("4. Running inference...")
    output = tester.run_inference(test_input)
    print(f"   Output shape: {output.shape}")
    print(f"   Output sample: {output[0, :3].tolist()}")

    # Run benchmark
    print("5. Running benchmark...")
    benchmark_results = tester.benchmark(test_input, num_runs=50)
    print(f"   Mean time: {benchmark_results['mean_time_ms']:.3f} ms")
    print(f"   Std time: {benchmark_results['std_time_ms']:.3f} ms")

    # Example comparison (with mock MAX output)
    print("6. Comparing outputs...")
    mock_max_output = output.detach().cpu().numpy()
    comparison = compare_outputs(output, mock_max_output)

    if comparison["passed"]:
        print("   ✅ Outputs match!")
    else:
        print("   ❌ Outputs differ!")
        print(f"   Max absolute difference: {comparison['max_abs_diff']}")

    # Save results
    print("7. Saving results...")
    results = {
        "model_info": {
            "input_size": 10,
            "output_size": 5,
            "total_params": sum(p.numel() for p in model.parameters()),
        },
        "benchmark": benchmark_results,
        "comparison": comparison,
    }

    save_test_results(results, "example_test_results.json")
    print("   Results saved to example_test_results.json")

    print("\n✅ Example completed successfully!")


if __name__ == "__main__":
    main()
