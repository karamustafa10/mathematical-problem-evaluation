"""
Test cases for the DataLoader class.
"""

import unittest
import os
import pandas as pd
import json
from src.data.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    """Test cases for DataLoader class."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_data_dir = 'test_data'
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        # Create sample CSV file
        self.csv_file = os.path.join(self.test_data_dir, 'sample.csv')
        df = pd.DataFrame({
            'problem_text': ['Problem 1', 'Problem 2'],
            'answer': ['Answer 1', 'Answer 2']
        })
        df.to_csv(self.csv_file, index=False)
        
        # Create sample JSON file
        self.json_file = os.path.join(self.test_data_dir, 'sample.json')
        data = [
            {'problem_text': 'Problem 1', 'answer': 'Answer 1'},
            {'problem_text': 'Problem 2', 'answer': 'Answer 2'}
        ]
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
            
    def tearDown(self):
        """Clean up test environment."""
        for file in os.listdir(self.test_data_dir):
            os.remove(os.path.join(self.test_data_dir, file))
        os.rmdir(self.test_data_dir)
        
    def test_load_data_csv(self):
        """Test loading data from CSV file."""
        loader = DataLoader(self.csv_file)
        data = loader.load_data()
        
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 2)
        self.assertIn('problem_text', data.columns)
        self.assertIn('answer', data.columns)
        
    def test_load_data_json(self):
        """Test loading data from JSON file."""
        loader = DataLoader(self.json_file)
        data = loader.load_data()
        
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 2)
        self.assertIn('problem_text', data.columns)
        self.assertIn('answer', data.columns)
        
    def test_invalid_file(self):
        """Test behavior with invalid file."""
        invalid_file = os.path.join(self.test_data_dir, 'invalid.txt')
        with open(invalid_file, 'w') as f:
            f.write('Invalid data')
            
        loader = DataLoader(invalid_file)
        with self.assertRaises(ValueError):
            loader.load_data()
            
    def test_missing_columns(self):
        """Test behavior with missing required columns."""
        # Create CSV with missing columns
        invalid_csv = os.path.join(self.test_data_dir, 'invalid.csv')
        df = pd.DataFrame({'other_column': ['Value 1', 'Value 2']})
        df.to_csv(invalid_csv, index=False)
        
        loader = DataLoader(invalid_csv)
        data = loader.load_data()
        
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 2)
        self.assertNotIn('problem_text', data.columns)
        self.assertNotIn('answer', data.columns)
        
    def test_preprocess_data(self):
        """Test data preprocessing."""
        loader = DataLoader(self.csv_file)
        data = loader.load_data()
        processed_data = loader.preprocess_data()
        
        self.assertIsInstance(processed_data, pd.DataFrame)
        self.assertEqual(len(processed_data), 2)
        self.assertTrue(processed_data['problem_text'].dtype == 'object')
        self.assertTrue(processed_data['answer'].dtype == 'object')
        
    def test_get_problem(self):
        """Test retrieving a specific problem."""
        loader = DataLoader(self.csv_file)
        loader.load_data()
        problem = loader.get_problem(0)
        
        self.assertIsInstance(problem, dict)
        self.assertIn('problem_text', problem)
        self.assertIn('answer', problem)
        self.assertEqual(problem['problem_text'], 'Problem 1')
        self.assertEqual(problem['answer'], 'Answer 1')
        
    def test_get_all_problems(self):
        """Test retrieving all problems."""
        loader = DataLoader(self.csv_file)
        loader.load_data()
        problems = loader.get_all_problems()
        
        self.assertIsInstance(problems, list)
        self.assertEqual(len(problems), 2)
        self.assertIsInstance(problems[0], dict)
        self.assertIn('problem_text', problems[0])
        self.assertIn('answer', problems[0])

if __name__ == '__main__':
    unittest.main() 