import json
import os
import csv
import random
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.problems = []
        self._load_problems()

    def _determine_category(self, question: str) -> str:
        """Determine the category of a problem based on its content."""
        question = question.lower()
        
        # Geometry related keywords
        geometry_keywords = ['circle', 'triangle', 'square', 'rectangle', 'angle', 'perimeter', 'area', 
                           'volume', 'surface', 'radius', 'diameter', 'circumference', 'parallel', 
                           'perpendicular', 'congruent', 'similar']
        
        # Algebra related keywords
        algebra_keywords = ['equation', 'inequality', 'function', 'polynomial', 'quadratic', 'linear',
                          'exponential', 'logarithm', 'matrix', 'determinant', 'vector']
        
        # Arithmetic related keywords
        arithmetic_keywords = ['sum', 'difference', 'product', 'quotient', 'fraction', 'decimal',
                             'percentage', 'ratio', 'proportion', 'average', 'mean', 'median']
        
        # Trigonometry related keywords
        trig_keywords = ['sine', 'cosine', 'tangent', 'cotangent', 'secant', 'cosecant', 'angle',
                        'degree', 'radian', 'sin', 'cos', 'tan', 'cot', 'sec', 'csc']
        
        # Count keyword matches for each category
        geometry_count = sum(1 for keyword in geometry_keywords if keyword in question)
        algebra_count = sum(1 for keyword in algebra_keywords if keyword in question)
        arithmetic_count = sum(1 for keyword in arithmetic_keywords if keyword in question)
        trig_count = sum(1 for keyword in trig_keywords if keyword in question)
        
        # Determine the category with the most matches
        counts = {
            'geometry': geometry_count,
            'algebra': algebra_count,
            'arithmetic': arithmetic_count,
            'trigonometry': trig_count
        }
        
        # If no matches found, default to 'general'
        if sum(counts.values()) == 0:
            return 'general'
            
        return max(counts.items(), key=lambda x: x[1])[0]

    def _load_problems(self) -> None:
        """Load problems from CSV files in the data directory."""
        try:
            # Get all CSV files in the data directory
            csv_files = [f for f in os.listdir(self.data_dir) if f.endswith('.csv')]
            
            if not csv_files:
                logger.warning("No CSV files found in data directory. Creating sample problem.")
                self._create_sample_problem()
                return

            # Load problems from each CSV file
            for csv_file in csv_files:
                file_path = os.path.join(self.data_dir, csv_file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            question = row.get('problem', '')
                            problem = {
                                'problem_id': row.get('problem_id', ''),
                                'question': question,
                                'correct_answer': row.get('answer', ''),
                                'solution': row.get('solution', ''),
                                'category': self._determine_category(question),
                                'difficulty': 'hard',  # AIME problems are generally hard
                                'source': csv_file
                            }
                            if problem['question'] and problem['correct_answer']:
                                self.problems.append(problem)
                except Exception as e:
                    logger.error(f"Error loading CSV file {csv_file}: {str(e)}")

            if not self.problems:
                logger.warning("No valid problems found in CSV files. Creating sample problem.")
                self._create_sample_problem()

        except Exception as e:
            logger.error(f"Error loading problems: {str(e)}")
            self._create_sample_problem()

    def _create_sample_problem(self) -> None:
        """Create a sample problem if no problems are found."""
        sample_problem = {
            'problem_id': 'sample_1',
            'question': 'What is the sum of all positive integers less than 100 that are divisible by 3?',
            'correct_answer': '1683',
            'category': 'arithmetic',
            'difficulty': 'medium',
            'source': 'sample'
        }
        self.problems = [sample_problem]
        
        # Save the sample problem
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            with open(os.path.join(self.data_dir, 'sample_problem.json'), 'w', encoding='utf-8') as f:
                json.dump(sample_problem, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving sample problem: {str(e)}")

    def get_random_problems(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get a random selection of problems."""
        if not self.problems:
            self._load_problems()
        
        # If we have fewer problems than requested, return all problems
        if len(self.problems) <= count:
            return self.problems
        
        # Otherwise, return a random selection
        return random.sample(self.problems, count)

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