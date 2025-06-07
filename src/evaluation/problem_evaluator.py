"""
Problem evaluator module for evaluating AI model responses to mathematical problems.
"""

import re
import logging
from typing import Dict, List, Optional, Any

class ProblemEvaluator:
    """Evaluates AI model responses to mathematical problems."""
    
    def __init__(self):
        """Initialize the ProblemEvaluator."""
        self.logger = logging.getLogger(__name__)
        
        # Define patterns for identifying solution components
        self.step_patterns = {
            'solution': r'(?:step|solution|solve|calculate|compute).*?(?=\n|$)',
            'answer': r'(?:answer|result|therefore|thus).*?(?=\n|$)',
            'explanation': r'(?:explain|because|since|as).*?(?=\n|$)'
        }
        
    def evaluate_responses(self, problem: Dict[str, str], responses: List[Dict[str, str]]) -> Dict[str, Dict[str, Any]]:
        """
        Evaluate model responses for a given problem.
        
        Args:
            problem: Dictionary containing problem text and answer
            responses: List of dictionaries containing model responses
            
        Returns:
            Dictionary containing evaluation results for each model
        """
        self.logger.info(f"Evaluating responses for problem: {problem.get('problem_text', 'unknown')}")
        
        results = {}
        for response in responses:
            model_name = response.get('model', 'unknown')
            response_text = response.get('response', '')
            
            # Extract and analyze steps
            steps = self._extract_steps(response_text)
            step_analysis = self._analyze_steps(response_text)
            
            # Check correctness
            is_correct = self._check_correctness(response_text, problem.get('answer', ''))
            
            # Extract answer
            extracted_answer = self._extract_answer(response_text)
            
            # Store results
            results[model_name] = {
                'is_correct': is_correct,
                'extracted_answer': extracted_answer,
                'step_analysis': step_analysis
            }
            
        return results
        
    def _extract_steps(self, response: str) -> List[str]:
        """
        Extract solution steps from model response.
        
        Args:
            response: Model's response text
            
        Returns:
            List of extracted steps
        """
        steps = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Remove step numbers and bullet points
            line = re.sub(r'^\d+\.\s*|^[-*]\s*', '', line)
            
            # Check if line contains any step pattern
            for pattern in self.step_patterns.values():
                if re.search(pattern, line, re.IGNORECASE):
                    steps.append(line)
                    break
                    
        return steps
        
    def _check_correctness(self, response: str, expected_answer: str) -> bool:
        """
        Check if the model's answer matches the expected answer.
        
        Args:
            response: Model's response text
            expected_answer: Expected answer
            
        Returns:
            True if answer is correct, False otherwise
        """
        extracted_answer = self._extract_answer(response)
        if not extracted_answer or not expected_answer:
            return False
            
        # Normalize answers for comparison
        extracted_answer = self._normalize_answer(extracted_answer)
        expected_answer = self._normalize_answer(expected_answer)
        
        return extracted_answer == expected_answer
        
    def _extract_answer(self, response: str) -> Optional[str]:
        """
        Extract the final answer from model response.
        
        Args:
            response: Model's response text
            
        Returns:
            Extracted answer or None if not found
        """
        # Look for answer pattern
        answer_pattern = r'(?:answer|result|therefore|thus)[^\d]*(\d+(?:\.\d+)?)'
        match = re.search(answer_pattern, response, re.IGNORECASE)
        
        if match:
            return match.group(1)
            
        # If no answer pattern found, try to find the last number in the response
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', response)
        if numbers:
            return numbers[-1]
            
        return None
        
    def _analyze_steps(self, response: str) -> Dict[str, Any]:
        """
        Analyze the solution steps in the response.
        
        Args:
            response: Model's response text
            
        Returns:
            Dictionary containing step analysis
        """
        steps = self._extract_steps(response)
        step_types = {}
        
        for step in steps:
            for step_type, pattern in self.step_patterns.items():
                if re.search(pattern, step, re.IGNORECASE):
                    step_types[step_type] = step_types.get(step_type, 0) + 1
                    break
            else:
                step_types['unknown'] = step_types.get('unknown', 0) + 1
                
        completeness = self._check_step_completeness(response)
        
        return {
            'step_count': len(steps),
            'step_types': step_types,
            'completeness': completeness
        }
        
    def _check_step_completeness(self, response: str) -> float:
        """
        Check the completeness of solution steps.
        
        Args:
            response: Model's response text
            
        Returns:
            Completeness score between 0 and 1
        """
        step_types = set()
        for step_type, pattern in self.step_patterns.items():
            if re.search(pattern, response, re.IGNORECASE):
                step_types.add(step_type)
                
        # Calculate completeness based on required step types
        required_types = {'solution', 'answer'}
        if not required_types:
            return 0.0
            
        return len(step_types.intersection(required_types)) / len(required_types)
        
    def _normalize_answer(self, answer: str) -> str:
        """
        Normalize answer for comparison.
        
        Args:
            answer: Answer string to normalize
            
        Returns:
            Normalized answer string
        """
        # Remove whitespace and convert to lowercase
        answer = answer.strip().lower()
        
        # Remove common units and symbols
        answer = re.sub(r'[^\d.]', '', answer)
        
        # Convert to float and back to string to normalize decimal format
        try:
            return str(float(answer))
        except ValueError:
            return answer 