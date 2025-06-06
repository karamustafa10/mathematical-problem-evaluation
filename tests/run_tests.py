"""
Test Runner Script

This script runs all test cases in the tests directory.
"""

import unittest
import sys
import os
from datetime import datetime

def run_tests():
    """Run all test cases and generate a report."""
    # Add project root to Python path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    
    # Create test results directory
    results_dir = os.path.join(project_root, 'test_results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Create test runner with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run tests and capture results
    print(f"\nRunning tests at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    result = runner.run(suite)
    
    # Generate test report
    report_file = os.path.join(
        results_dir,
        f'test_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    )
    
    with open(report_file, 'w') as f:
        f.write(f"Test Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        # Summary
        f.write("Test Summary:\n")
        f.write(f"Tests run: {result.testsRun}\n")
        f.write(f"Failures: {len(result.failures)}\n")
        f.write(f"Errors: {len(result.errors)}\n")
        f.write(f"Skipped: {len(result.skipped)}\n\n")
        
        # Failures
        if result.failures:
            f.write("Failures:\n")
            f.write("-" * 40 + "\n")
            for failure in result.failures:
                f.write(f"{failure[0]}\n")
                f.write(f"{failure[1]}\n\n")
                
        # Errors
        if result.errors:
            f.write("Errors:\n")
            f.write("-" * 40 + "\n")
            for error in result.errors:
                f.write(f"{error[0]}\n")
                f.write(f"{error[1]}\n\n")
                
        # Skipped
        if result.skipped:
            f.write("Skipped:\n")
            f.write("-" * 40 + "\n")
            for skip in result.skipped:
                f.write(f"{skip[0]}\n")
                f.write(f"{skip[1]}\n\n")
                
    print(f"\nTest report saved to: {report_file}")
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1
    
if __name__ == '__main__':
    sys.exit(run_tests()) 