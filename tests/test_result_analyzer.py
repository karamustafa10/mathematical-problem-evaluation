"""
Test module for the ResultAnalyzer class.
"""

import unittest
import os
import json
import pandas as pd
from src.evaluation.result_analyzer import ResultAnalyzer

class TestResultAnalyzer(unittest.TestCase):
    """Test cases for the ResultAnalyzer class."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = 'test_analysis'
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Create sample results file
        self.sample_results = {
            'problem1': {
                'category': 'geometry',
                'model1': {
                    'is_correct': True,
                    'steps': ['Step 1', 'Step 2'],
                    'error_type': None,
                    'response_time': 1.5
                },
                'model2': {
                    'is_correct': False,
                    'steps': ['Step 1'],
                    'error_type': 'calculation_error',
                    'response_time': 2.0
                }
            },
            'problem2': {
                'category': 'algebra',
                'model1': {
                    'is_correct': True,
                    'steps': ['Step 1', 'Step 2', 'Step 3'],
                    'error_type': None,
                    'response_time': 1.8
                },
                'model2': {
                    'is_correct': True,
                    'steps': ['Step 1', 'Step 2'],
                    'error_type': None,
                    'response_time': 1.6
                }
            }
        }
        
        self.results_file = os.path.join(self.test_dir, 'sample_results.json')
        with open(self.results_file, 'w') as f:
            json.dump(self.sample_results, f)
            
        self.analyzer = ResultAnalyzer(self.results_file)
        
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.results_file):
            os.remove(self.results_file)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
            
    def test_calculate_metrics(self):
        """Test calculation of evaluation metrics."""
        metrics = self.analyzer.calculate_metrics()
        
        self.assertIsInstance(metrics, dict)
        self.assertIn('overall_accuracy', metrics)
        self.assertIn('category_accuracy', metrics)
        self.assertIn('step_completeness', metrics)
        self.assertIn('error_distribution', metrics)
        self.assertIn('response_times', metrics)
        self.assertIn('model_comparison', metrics)
        
    def test_generate_visualizations(self):
        """Test generation of visualization files."""
        output_dir = os.path.join(self.test_dir, 'visualizations')
        self.analyzer.generate_visualizations(output_dir)
        
        # Check if visualization files were created
        expected_files = [
            'overall_accuracy.png',
            'category_accuracy.png',
            'step_completeness.png',
            'error_distribution.png',
            'response_times.png',
            'model_comparison.png'
        ]
        
        for file in expected_files:
            file_path = os.path.join(output_dir, file)
            self.assertTrue(os.path.exists(file_path))
            
    def test_generate_report(self):
        """Test generation of analysis report."""
        report_file = self.analyzer.generate_report(self.test_dir)
        
        self.assertTrue(os.path.exists(report_file))
        self.assertTrue(report_file.endswith('.md'))
        
        # Check report content
        with open(report_file, 'r') as f:
            content = f.read()
            self.assertIn('Overall Results', content)
            self.assertIn('Category Analysis', content)
            self.assertIn('Model Comparison', content)
            
    def test_empty_results(self):
        """Test behavior with empty results file."""
        empty_file = os.path.join(self.test_dir, 'empty_results.json')
        with open(empty_file, 'w') as f:
            json.dump({}, f)
            
        analyzer = ResultAnalyzer(empty_file)
        metrics = analyzer.calculate_metrics()
        
        self.assertIsInstance(metrics, dict)
        self.assertEqual(metrics['overall_accuracy'], 0)
        self.assertEqual(len(metrics['category_accuracy']), 0)
        
        os.remove(empty_file)
        
    def test_invalid_results(self):
        """Test behavior with invalid results file."""
        invalid_file = os.path.join(self.test_dir, 'invalid_results.json')
        with open(invalid_file, 'w') as f:
            f.write('invalid json content')
            
        with self.assertRaises(Exception):
            ResultAnalyzer(invalid_file)
            
        os.remove(invalid_file)
        
    def test_missing_data(self):
        """Test behavior with missing data in results."""
        incomplete_results = {
            'problem1': {
                'category': 'geometry',
                'model1': {
                    'is_correct': True
                    # Missing other fields
                }
            }
        }
        
        incomplete_file = os.path.join(self.test_dir, 'incomplete_results.json')
        with open(incomplete_file, 'w') as f:
            json.dump(incomplete_results, f)
            
        analyzer = ResultAnalyzer(incomplete_file)
        metrics = analyzer.calculate_metrics()
        
        self.assertIsInstance(metrics, dict)
        self.assertIn('overall_accuracy', metrics)
        
        os.remove(incomplete_file)
        
if __name__ == '__main__':
    unittest.main() 