"""
Data Loader Module for Mathematical Problem Evaluation System.

This module handles the loading and processing of mathematical problems from various sources,
including CSV files and sample problems. It provides functionality to load, validate, and
prepare problems for evaluation.
"""

import json
import os
import csv
import random
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Class for loading and managing mathematical problems.
    
    This class provides methods to:
    - Load problems from CSV files
    - Create and save sample problems
    - Get random problems for evaluation
    - Validate problem structure
    """

    def __init__(self):
        """Initialize the DataLoader with necessary paths and configurations."""
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        self.sample_file = os.path.join(self.data_dir, 'sample_problem.json')
        self._ensure_data_directory()

    def _ensure_data_directory(self) -> None:
        """
        Ensure the data directory exists.
        
        Creates the data directory if it doesn't exist and initializes it with
        a sample problem if no problems are found.
        """
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory at {self.data_dir}")
            self._create_sample_problem()

    def _create_sample_problem(self) -> None:
        """
        Create and save a sample mathematical problem.
        
        This method creates a sample problem with a circle-related question
        and saves it to the data directory.
        """
        sample_problem = {
            'problem_id': 'sample_1',
            'question': 'What is the area of a circle with radius 5?',
            'correct_answer': '25π',
            'solution': 'The area of a circle is given by A = πr². For r = 5, A = π(5)² = 25π.',
            'category': 'geometry',
            'difficulty': 'medium'
        }
        
        with open(self.sample_file, 'w') as f:
            json.dump(sample_problem, f, indent=4)
        logger.info(f"Created sample problem at {self.sample_file}")

    def _load_problems(self) -> List[Dict[str, Any]]:
        """
        Load problems from CSV files in the data directory.
        
        Returns:
            List of problems loaded from CSV files. If no problems are found,
            returns a list containing the sample problem.
        """
        problems = []
        csv_files = [f for f in os.listdir(self.data_dir) if f.endswith('.csv')]
        
        if not csv_files:
            logger.warning("No CSV files found in data directory. Using sample problem.")
            if os.path.exists(self.sample_file):
                with open(self.sample_file, 'r') as f:
                    problems.append(json.load(f))
            return problems

        for csv_file in csv_files:
            try:
                with open(os.path.join(self.data_dir, csv_file), 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        problem = {
                            'problem_id': row.get('problem_id', ''),
                            'question': row.get('problem', ''),
                            'correct_answer': row.get('answer', ''),
                            'solution': row.get('solution', ''),
                            'category': self._determine_category(row.get('problem', '')),
                            'difficulty': 'hard'  # AIME problems are hard
                        }
                        if self._validate_problem(problem):
                            problems.append(problem)
            except Exception as e:
                logger.error(f"Error loading {csv_file}: {str(e)}")

        if not problems:
            logger.warning("No valid problems found in CSV files. Using sample problem.")
            if os.path.exists(self.sample_file):
                with open(self.sample_file, 'r') as f:
                    problems.append(json.load(f))

        return problems

    def _validate_problem(self, problem: Dict[str, Any]) -> bool:
        """
        Validate the structure and content of a problem.
        
        Args:
            problem: Dictionary containing problem data.
            
        Returns:
            True if the problem is valid, False otherwise.
        """
        required_fields = ['problem_id', 'question', 'correct_answer']
        return all(problem.get(field) for field in required_fields)

    def _determine_category(self, question: str) -> str:
        """
        Determine the category of a problem based on its content.
        
        Args:
            question: The problem question text.
            
        Returns:
            String representing the problem category.
        """
        question = question.lower()
        if 'circle' in question:
            return 'geometry'
        elif any(word in question for word in ['function', 'equation', 'solve']):
            return 'algebra'
        elif any(word in question for word in ['probability', 'chance']):
            return 'probability'
        elif any(word in question for word in ['sequence', 'series']):
            return 'sequences'
        else:
            return 'unknown'

    def get_random_problems(self, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get a random selection of problems for evaluation.
        
        Args:
            count: Number of problems to select.
            
        Returns:
            List of randomly selected problems.
        """
        problems = self._load_problems()
        if not problems:
            logger.error("No problems available for selection.")
            return []
            
        count = min(count, len(problems))
        return random.sample(problems, count)

    def get_all_problems(self) -> List[Dict[str, Any]]:
        """Get all available problems."""
        if not self.problems:
            self._load_problems()
        return self.problems

    def save_problems(self, problems: List[Dict[str, Any]], filename: str) -> None:
        """Save problems to a JSON file."""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            file_path = os.path.join(self.data_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(problems, f, indent=2, ensure_ascii=False)
            logger.info(f"Problems saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving problems: {str(e)}") 