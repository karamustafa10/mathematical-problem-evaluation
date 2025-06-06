"""
Test module for the ProblemEvaluator class.
"""

import unittest
from src.evaluation.problem_evaluator import ProblemEvaluator

class TestProblemEvaluator(unittest.TestCase):
    """Test cases for the ProblemEvaluator class."""
    
    def setUp(self):
        """Set up test environment."""
        self.evaluator = ProblemEvaluator()
        
        # Sample problem data
        self.sample_problem = {
            'question': 'What is the area of a circle with radius 5?',
            'solution': 'The area of a circle is πr². So, A = π(5)² = 25π',
            'answer': '25π'
        }
        
        # Sample model responses
        self.sample_responses = {
            'model1': {
                'response': 'The area is πr². For r=5, A=π(5)²=25π',
                'steps': ['Use formula A=πr²', 'Substitute r=5', 'Calculate A=25π']
            },
            'model2': {
                'response': 'Area = πr² = π(5)² = 25π',
                'steps': ['Use area formula', 'Calculate 5²', 'Multiply by π']
            }
        }
        
    def test_evaluate_responses(self):
        """Test evaluation of model responses."""
        results = self.evaluator.evaluate_responses(
            self.sample_problem,
            self.sample_responses
        )
        
        self.assertIsInstance(results, dict)
        self.assertIn('model1', results)
        self.assertIn('model2', results)
        
        # Check evaluation structure
        for model_result in results.values():
            self.assertIn('is_correct', model_result)
            self.assertIn('steps', model_result)
            self.assertIn('error_type', model_result)
            
    def test_extract_steps(self):
        """Test step extraction from responses."""
        steps = self.evaluator._extract_steps(
            self.sample_responses['model1']['response']
        )
        
        self.assertIsInstance(steps, list)
        self.assertTrue(len(steps) > 0)
        
    def test_check_correctness(self):
        """Test correctness checking of responses."""
        is_correct = self.evaluator._check_correctness(
            self.sample_problem['answer'],
            self.sample_responses['model1']['response']
        )
        
        self.assertIsInstance(is_correct, bool)
        
    def test_extract_answer(self):
        """Test answer extraction from responses."""
        answer = self.evaluator._extract_answer(
            self.sample_responses['model1']['response']
        )
        
        self.assertIsInstance(answer, str)
        self.assertTrue(len(answer) > 0)
        
    def test_analyze_steps(self):
        """Test step analysis of responses."""
        analysis = self.evaluator._analyze_steps(
            self.sample_responses['model1']['steps']
        )
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('completeness', analysis)
        self.assertIn('clarity', analysis)
        
    def test_check_step_completeness(self):
        """Test step completeness checking."""
        completeness = self.evaluator._check_step_completeness(
            self.sample_responses['model1']['steps']
        )
        
        self.assertIsInstance(completeness, float)
        self.assertTrue(0 <= completeness <= 1)
        
    def test_invalid_response(self):
        """Test handling of invalid response format."""
        invalid_responses = {
            'model1': {
                'response': '',  # Empty response
                'steps': []
            }
        }
        
        results = self.evaluator.evaluate_responses(
            self.sample_problem,
            invalid_responses
        )
        
        self.assertIsInstance(results, dict)
        self.assertIn('model1', results)
        self.assertFalse(results['model1']['is_correct'])
        
    def test_missing_steps(self):
        """Test handling of responses without steps."""
        responses_without_steps = {
            'model1': {
                'response': 'The answer is 25π',
                'steps': []  # Empty steps
            }
        }
        
        results = self.evaluator.evaluate_responses(
            self.sample_problem,
            responses_without_steps
        )
        
        self.assertIsInstance(results, dict)
        self.assertIn('model1', results)
        self.assertIn('steps', results['model1'])
        
if __name__ == '__main__':
    unittest.main() 