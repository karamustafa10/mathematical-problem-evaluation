"""
Test module for the DataLoader class.
"""

import unittest
import os
import pandas as pd
from src.data.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    """Test cases for the DataLoader class."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_data_dir = 'test_data'
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        # Create sample CSV file
        self.sample_data = pd.DataFrame({
            'question': ['Test question 1', 'Test question 2'],
            'solution': ['Test solution 1', 'Test solution 2'],
            'answer': ['A', 'B']
        })
        self.sample_file = os.path.join(self.test_data_dir, 'sample.csv')
        self.sample_data.to_csv(self.sample_file, index=False)
        
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.sample_file):
            os.remove(self.sample_file)
        if os.path.exists(self.test_data_dir):
            os.rmdir(self.test_data_dir)
            
    def test_load_data(self):
        """Test loading data from CSV file."""
        loader = DataLoader(self.test_data_dir)
        data = loader.load_data()
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertIn('question', data[0])
        self.assertIn('solution', data[0])
        self.assertIn('answer', data[0])
        
    def test_empty_directory(self):
        """Test behavior with empty directory."""
        empty_dir = 'empty_test_data'
        os.makedirs(empty_dir, exist_ok=True)
        
        loader = DataLoader(empty_dir)
        data = loader.load_data()
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)
        
        os.rmdir(empty_dir)
        
    def test_invalid_file(self):
        """Test behavior with invalid CSV file."""
        invalid_file = os.path.join(self.test_data_dir, 'invalid.csv')
        with open(invalid_file, 'w') as f:
            f.write('invalid,csv,data\n')
            
        loader = DataLoader(self.test_data_dir)
        data = loader.load_data()
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)  # Should still load valid file
        
        os.remove(invalid_file)
        
    def test_missing_columns(self):
        """Test behavior with missing required columns."""
        invalid_data = pd.DataFrame({
            'question': ['Test question'],
            'solution': ['Test solution']
            # Missing 'answer' column
        })
        invalid_file = os.path.join(self.test_data_dir, 'invalid.csv')
        invalid_data.to_csv(invalid_file, index=False)
        
        loader = DataLoader(self.test_data_dir)
        data = loader.load_data()
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)  # Should still load valid file
        
        os.remove(invalid_file)
        
if __name__ == '__main__':
    unittest.main() 