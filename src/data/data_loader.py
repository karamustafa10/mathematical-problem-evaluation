"""
Data loading and preprocessing module.

This module provides functionality for loading and preprocessing mathematical problem data.
"""

import pandas as pd
import json
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """Class for loading and preprocessing mathematical problem data."""
    
    def __init__(self, data_path: str):
        """
        Initialize the DataLoader.
        
        Args:
            data_path (str): Path to the data file (CSV or JSON)
        """
        self.data_path = data_path
        self.data = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load data from the specified path.
        
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            if self.data_path.endswith('.csv'):
                self.data = pd.read_csv(self.data_path)
            elif self.data_path.endswith('.json'):
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    self.data = pd.DataFrame(json.load(f))
            else:
                raise ValueError("Unsupported file format. Use CSV or JSON.")
            
            logger.info(f"Successfully loaded data from {self.data_path}")
            return self.data
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
            
    def preprocess_data(self) -> pd.DataFrame:
        """
        Preprocess the loaded data.
        
        Returns:
            pd.DataFrame: Preprocessed data
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
            
        try:
            # Remove any rows with missing values
            self.data = self.data.dropna()
            
            # Convert problem text to string type
            if 'problem_text' in self.data.columns:
                self.data['problem_text'] = self.data['problem_text'].astype(str)
                
            # Convert answer to string type
            if 'answer' in self.data.columns:
                self.data['answer'] = self.data['answer'].astype(str)
                
            logger.info("Data preprocessing completed successfully")
            return self.data
            
        except Exception as e:
            logger.error(f"Error preprocessing data: {str(e)}")
            raise
            
    def get_problem(self, index: int) -> Dict:
        """
        Get a specific problem by index.
        
        Args:
            index (int): Index of the problem to retrieve
            
        Returns:
            Dict: Problem data
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
            
        try:
            problem = self.data.iloc[index].to_dict()
            return problem
            
        except Exception as e:
            logger.error(f"Error retrieving problem at index {index}: {str(e)}")
            raise
            
    def get_all_problems(self) -> List[Dict]:
        """
        Get all problems in the dataset.
        
        Returns:
            List[Dict]: List of all problems
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
            
        try:
            problems = self.data.to_dict('records')
            return problems
            
        except Exception as e:
            logger.error(f"Error retrieving all problems: {str(e)}")
            raise 