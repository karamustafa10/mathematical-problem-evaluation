"""
Problem Evaluator Module for Mathematical Problem Evaluation System.

This module handles the evaluation of AI model responses to mathematical problems.
It provides functionality to compare model responses with correct answers and
generate detailed evaluation results.
"""

import re
import json
import logging
from typing import Dict, List, Optional, Any
import math

logger = logging.getLogger(__name__)

class ProblemEvaluator:
    """
    Class for evaluating AI model responses to mathematical problems.
    
    This class provides methods to:
    - Evaluate model responses against correct answers
    - Normalize and compare mathematical expressions
    - Generate detailed evaluation results
    """

    def __init__(self):
        """Initialize the ProblemEvaluator with necessary configurations."""
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('evaluation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Define step patterns for solution analysis
        self.step_patterns = {
            'calculation': r'\d+\s*[\+\-\*\/]\s*\d+\s*=\s*\d+',  # Basic arithmetic
            'equation': r'[a-zA-Z]\s*=\s*\d+',  # Variable assignment
            'formula': r'[a-zA-Z]\([^)]+\)\s*=\s*\d+',  # Function application
            'explanation': r'(?:because|since|therefore|thus|hence|as a result)',  # Reasoning
            'substitution': r'(?:substituting|replacing|plugging in)',  # Value substitution
            'simplification': r'(?:simplifying|reducing|combining)',  # Expression simplification
            'verification': r'(?:checking|verifying|confirming)',  # Solution verification
            'conclusion': r'(?:therefore|thus|hence|we get|we obtain)'  # Final answer
        }

    def evaluate_responses(self, problem: Dict[str, Any], responses: Dict[str, str]) -> Dict[str, Any]:
        """
        Evaluate responses from different models for a given problem.
        
        Args:
            problem: Dictionary containing problem data including question and correct answer.
            responses: Dictionary of model responses to evaluate.
            
        Returns:
            Dictionary containing evaluation results for each model's response.
        """
        try:
            self.logger.info(f"Evaluating responses for problem: {problem.get('problem_id', 'unknown')}")
            
            # Initialize results structure
            results = {
                "problem_id": problem.get("problem_id", "unknown"),
                "question": problem.get("question", ""),
                "correct_answer": problem.get("correct_answer", ""),
                "model_evaluations": {}
            }
            model_categories = problem.get('model_categories', {})
            
            # Evaluate each model's response
            for model_name, response in responses.items():
                self.logger.info(f"Evaluating {model_name}'s response")
                
                predicted_category = None
                # Eğer response bir dict ise, çözüm ve kategori ayrıştır
                if isinstance(response, dict):
                    solution = response.get('solution', None)
                    predicted_category = response.get('category', None)
                    response_text = solution
                else:
                    response_text = response
                    predicted_category = model_categories.get(model_name) if model_categories else None
                
                if response_text is None:
                    # Handle None response
                    results["model_evaluations"][model_name] = {
                        "response": None,
                        "predicted_category": predicted_category,
                        "correctness": {
                            "is_correct": False,
                            "matched_answer": None,
                            "error": "No response received from model"
                        },
                        "step_analysis": {
                            "step_count": 0,
                            "step_types": {},
                            "completeness": False
                        }
                    }
                    continue
                
                # Extract steps and check correctness
                steps = self._extract_steps(response_text)
                is_correct = self._check_correctness(response_text, problem.get("correct_answer", ""))
                step_analysis = self._analyze_steps(steps)
                
                # Store evaluation results
                results["model_evaluations"][model_name] = {
                    "response": response_text,
                    "predicted_category": predicted_category,
                    "correctness": {
                        "is_correct": is_correct,
                        "matched_answer": self._extract_answer(response_text)
                    },
                    "step_analysis": step_analysis
                }
            
            self.logger.info("Evaluation completed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in evaluate_responses: {str(e)}")
            raise

    def _extract_steps(self, response: str) -> List[Dict[str, str]]:
        """
        Extract solution steps from a model's response.
        
        Args:
            response: The complete response text from the model.
            
        Returns:
            List of dictionaries containing step type and content.
        """
        if not response:
            return []
            
        steps = []
        
        # Split response into lines
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check each step pattern
            for step_type, pattern in self.step_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    steps.append({
                        "type": step_type,
                        "content": line
                    })
                    break
        
        return steps

    def _check_correctness(self, response: str, correct_answer: str) -> bool:
        """
        Check if a response contains the correct answer.
        
        Args:
            response: The model's response text.
            correct_answer: The correct answer to check against.
            
        Returns:
            True if the correct answer is found in the response, False otherwise.
        """
        if not response or not correct_answer:
            return False
            
        try:
            # Extract numbers from response
            numbers = re.findall(r'\b\d+\b', response)
            
            # Check if correct answer is in the numbers
            return str(correct_answer) in numbers
            
        except Exception as e:
            self.logger.error(f"Error checking correctness: {str(e)}")
            return False

    def _extract_answer(self, response: str) -> Optional[str]:
        """
        Extract the final answer from a model's response.
        
        Args:
            response: The model's response text.
            
        Returns:
            The extracted answer as a string, or None if no answer is found.
        """
        if not response:
            return None
            
        try:
            # Look for common answer patterns
            patterns = [
                r'answer[:\s]+(\d+)',
                r'solution[:\s]+(\d+)',
                r'result[:\s]+(\d+)',
                r'(\d+)(?:\s*$|\s*[\.\n])'  # Number at end of line or followed by period/newline
            ]
            
            for pattern in patterns:
                match = re.search(pattern, response, re.IGNORECASE)
                if match:
                    return match.group(1)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error extracting answer: {str(e)}")
            return None

    def _analyze_steps(self, steps: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Analyze the solution steps in a model's response.
        
        Args:
            steps: List of step dictionaries containing type and content.
            
        Returns:
            Dictionary containing step analysis results.
        """
        try:
            # Count steps by type
            step_counts = {}
            step_sequence = []
            
            for step in steps:
                step_type = step["type"]
                if step_type not in step_counts:
                    step_counts[step_type] = 0
                step_counts[step_type] += 1
                step_sequence.append(step_type)
            
            # Check step completeness
            completeness = self._check_step_completeness(step_sequence)
            
            return {
                "step_count": len(steps),
                "step_types": step_counts,
                "completeness": completeness
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing steps: {str(e)}")
            return {
                "step_count": 0,
                "step_types": {},
                "completeness": False
            }

    def _check_step_completeness(self, step_sequence: List[str]) -> bool:
        """
        Check if the solution steps follow a logical sequence.
        
        Args:
            step_sequence: List of step types in order of appearance.
            
        Returns:
            True if the steps follow a logical sequence, False otherwise.
        """
        if not step_sequence:
            return False
            
        # Define expected step sequence
        expected_sequence = [
            'explanation',
            'substitution',
            'calculation',
            'simplification',
            'verification',
            'conclusion'
        ]
        
        # Check if all expected steps are present
        return all(step in step_sequence for step in expected_sequence) 