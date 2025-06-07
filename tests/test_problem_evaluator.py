"""
Test cases for the ProblemEvaluator class.
"""

import unittest
from src.evaluation.problem_evaluator import ProblemEvaluator

class TestProblemEvaluator(unittest.TestCase):
    """Test cases for ProblemEvaluator class."""
    
    def setUp(self):
        """Set up test environment."""
        self.evaluator = ProblemEvaluator()
        
        # Sample problem data
        self.problem = {
            'problem_text': 'Solve for x: 2x + 5 = 13',
            'answer': '4'
        }
        
        # Sample model responses
        self.correct_response = {
            'model': 'test_model',
            'response': 'Step 1: Subtract 5 from both sides to get 2x = 8.\nStep 2: Divide both sides by 2 to get x = 4.\nAnswer: 4'
        }
        
        self.incorrect_response = {
            'model': 'test_model',
            'response': 'Step 1: Subtract 5 from both sides to get 2x = 8.\nStep 2: Divide both sides by 2 to get x = 3.\nAnswer: 3'
        }
        
        self.incomplete_response = {
            'model': 'test_model',
            'response': 'The answer is 4'
        }
        
    def test_extract_steps(self):
        """Test step extraction from model response."""
        steps = self.evaluator._extract_steps(self.correct_response['response'])
        
        self.assertIsInstance(steps, list)
        self.assertEqual(len(steps), 3)
        self.assertIn('subtract 5 from both sides', steps[0])
        self.assertIn('divide both sides by 2', steps[1])
        self.assertIn('Therefore', steps[2])
        
    def test_check_correctness(self):
        """Test answer correctness checking."""
        is_correct = self.evaluator._check_correctness(
            self.correct_response['response'],
            self.problem['answer']
        )
        
        self.assertTrue(is_correct)
        
        is_incorrect = self.evaluator._check_correctness(
            self.incorrect_response['response'],
            self.problem['answer']
        )
        
        self.assertFalse(is_incorrect)
        
    def test_extract_answer(self):
        """Test answer extraction from model response."""
        answer = self.evaluator._extract_answer(self.correct_response['response'])
        self.assertEqual(answer, '4')
        
        answer = self.evaluator._extract_answer(self.incorrect_response['response'])
        self.assertEqual(answer, '3')
        
    def test_analyze_steps(self):
        """Test step analysis."""
        analysis = self.evaluator._analyze_steps(self.correct_response['response'])
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('step_count', analysis)
        self.assertIn('step_types', analysis)
        self.assertIn('completeness', analysis)
        self.assertEqual(analysis['step_count'], 3)
        self.assertIn('solution', analysis['step_types'])
        self.assertIn('answer', analysis['step_types'])
        
    def test_check_step_completeness(self):
        """Test step completeness checking."""
        completeness = self.evaluator._check_step_completeness(
            self.correct_response['response']
        )
        
        self.assertIsInstance(completeness, float)
        self.assertGreater(completeness, 0.5)
        
        incomplete_completeness = self.evaluator._check_step_completeness(
            self.incomplete_response['response']
        )
        
        self.assertLess(incomplete_completeness, 0.5)
        
    def test_evaluate_responses(self):
        """Test response evaluation."""
        responses = [self.correct_response, self.incorrect_response]
        results = self.evaluator.evaluate_responses(self.problem, responses)
        
        self.assertIsInstance(results, dict)
        self.assertIn('test_model', results)
        self.assertIn('is_correct', results['test_model'])
        self.assertIn('extracted_answer', results['test_model'])
        self.assertIn('step_analysis', results['test_model'])
        
        # Check first response (correct)
        self.assertTrue(results['test_model']['is_correct'])
        self.assertEqual(results['test_model']['extracted_answer'], '4')
        
        # Check second response (incorrect)
        self.assertFalse(results['test_model']['is_correct'])
        self.assertEqual(results['test_model']['extracted_answer'], '3')
        
if __name__ == '__main__':
    unittest.main() 