import re
import json
import logging
from typing import Dict, List, Optional, Any

class ProblemEvaluator:
    def __init__(self):
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
        
        # Define step patterns
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
        Evaluate responses from different models for a given problem
        
        Args:
            problem (Dict): Problem data including question and correct answer
            responses (Dict): Dictionary of model responses
            
        Returns:
            Dict: Evaluation results
        """
        try:
            self.logger.info(f"Evaluating responses for problem: {problem.get('problem_id', 'unknown')}")
            
            # Initialize results
            results = {
                "problem_id": problem.get("problem_id", "unknown"),
                "question": problem.get("question", ""),
                "correct_answer": problem.get("correct_answer", ""),
                "model_evaluations": {}
            }
            
            # Evaluate each model's response
            for model_name, response in responses.items():
                self.logger.info(f"Evaluating {model_name}'s response")
                
                # Extract steps and check correctness
                steps = self._extract_steps(response)
                is_correct = self._check_correctness(response, problem.get("correct_answer", ""))
                step_analysis = self._analyze_steps(steps)
                
                # Store evaluation results
                results["model_evaluations"][model_name] = {
                    "response": response,
                    "correctness": {
                        "is_correct": is_correct,
                        "matched_answer": self._extract_answer(response)
                    },
                    "step_analysis": step_analysis
                }
            
            self.logger.info("Evaluation completed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in evaluate_responses: {str(e)}")
            raise

    def _extract_steps(self, response: str) -> List[Dict[str, str]]:
        """Extract solution steps from response"""
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
        """Check if response contains correct answer"""
        try:
            # Extract numbers from response
            numbers = re.findall(r'\b\d+\b', response)
            
            # Check if correct answer is in the numbers
            return str(correct_answer) in numbers
            
        except Exception as e:
            self.logger.error(f"Error checking correctness: {str(e)}")
            return False

    def _extract_answer(self, response: str) -> Optional[str]:
        """Extract final answer from response"""
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
        """Analyze solution steps"""
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
            
            return {
                "step_count": len(steps),
                "step_types": step_counts,
                "step_sequence": step_sequence,
                "is_complete": self._check_step_completeness(step_sequence)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing steps: {str(e)}")
            return {
                "step_count": 0,
                "step_types": {},
                "step_sequence": [],
                "is_complete": False
            }

    def _check_step_completeness(self, step_sequence: List[str]) -> bool:
        """Check if solution steps form a complete solution"""
        # Define required step types for a complete solution
        required_steps = {'calculation', 'conclusion'}
        
        # Check if all required steps are present
        return all(step in step_sequence for step in required_steps) 