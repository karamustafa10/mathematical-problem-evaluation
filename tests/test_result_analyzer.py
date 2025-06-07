"""
Test cases for the ResultAnalyzer class.
"""

import unittest
import os
import json
import pandas as pd
from src.evaluation.result_analyzer import ResultAnalyzer

class TestResultAnalyzer(unittest.TestCase):
    """Test cases for ResultAnalyzer class."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = 'test_results'
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Sample evaluation results
        self.sample_results = {
            'model1': {
                'is_correct': True,
                'extracted_answer': '4',
                'step_analysis': {
                    'step_count': 3,
                    'step_types': ['solution', 'answer'],
                    'completeness': 0.8
                }
            },
            'model2': {
                'is_correct': False,
                'extracted_answer': '3',
                'step_analysis': {
                    'step_count': 2,
                    'step_types': ['solution'],
                    'completeness': 0.4
                }
            }
        }
        
        # Save sample results to file
        self.results_file = os.path.join(self.test_dir, 'sample_results.json')
        with open(self.results_file, 'w', encoding='utf-8') as f:
            json.dump(self.sample_results, f)
            
        self.analyzer = ResultAnalyzer(self.results_file)
        
    def tearDown(self):
        """Clean up test environment."""
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)
        
    def test_load_results(self):
        """Test loading results from file."""
        self.analyzer.load_results()
        
        self.assertIsNotNone(self.analyzer.results)
        self.assertIn('model1', self.analyzer.results)
        self.assertIn('model2', self.analyzer.results)
        
    def test_calculate_metrics(self):
        """Test metrics calculation."""
        self.analyzer.load_results()
        metrics = self.analyzer.calculate_metrics()
        
        self.assertIsInstance(metrics, dict)
        self.assertIn('overall_accuracy', metrics)
        self.assertIn('model_performance', metrics)
        self.assertIn('step_completeness', metrics)
        
        # Check overall accuracy
        self.assertEqual(metrics['overall_accuracy'], 0.5)
        
        # Check model performance
        self.assertIn('model1', metrics['model_performance'])
        self.assertIn('model2', metrics['model_performance'])
        self.assertTrue(metrics['model_performance']['model1']['accuracy'])
        self.assertFalse(metrics['model_performance']['model2']['accuracy'])
        
        # Check step completeness
        self.assertIn('model1', metrics['step_completeness'])
        self.assertIn('model2', metrics['step_completeness'])
        self.assertEqual(metrics['step_completeness']['model1'], 0.8)
        self.assertEqual(metrics['step_completeness']['model2'], 0.4)
        
    def test_generate_visualizations(self):
        """Test visualization generation."""
        os.makedirs(self.test_dir, exist_ok=True)
        self.analyzer.load_results()
        self.analyzer.generate_visualizations()
        
        # Check if visualization files exist
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'accuracy_comparison.png')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'step_completeness.png')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'step_count_distribution.png')))
        
    def test_generate_report(self):
        """Test report generation."""
        self.analyzer.load_results()
        report_path = self.analyzer.generate_report()
        
        self.assertTrue(os.path.exists(report_path))
        
        # Read and check report content
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        self.assertIn('Overall Results', content)
        self.assertIn('Model Performance', content)
        self.assertIn('Step Completeness', content)
        self.assertIn('Visualizations', content)
        
    def test_invalid_results_file(self):
        """Test behavior with invalid results file."""
        invalid_file = os.path.join(self.test_dir, 'invalid.json')
        with open(invalid_file, 'w') as f:
            f.write('invalid json')
            
        analyzer = ResultAnalyzer(invalid_file)
        with self.assertRaises(ValueError):
            analyzer.load_results()
            
    def test_empty_results(self):
        """Test behavior with empty results."""
        empty_file = os.path.join(self.test_dir, 'empty.json')
        with open(empty_file, 'w') as f:
            json.dump({}, f)
            
        analyzer = ResultAnalyzer(empty_file)
        analyzer.load_results()
        
        with self.assertRaises(ValueError):
            analyzer.calculate_metrics()
        
if __name__ == '__main__':
    unittest.main() 