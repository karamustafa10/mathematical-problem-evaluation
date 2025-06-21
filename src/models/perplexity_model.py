"""
Perplexity Model Module for Mathematical Problem Evaluation System.

This module provides an interface to interact with Perplexity's AI model
for solving mathematical problems. It handles API communication, response
generation, and error handling.
"""

import os
import requests
from typing import Optional
import logging
import time
from utils.config import Config

logger = logging.getLogger(__name__)

class PerplexityModel:
    """
    Interface for interacting with Perplexity's AI model.
    
    This class provides methods to:
    - Initialize the Perplexity model with API credentials
    - Generate responses to mathematical problems
    - Handle API errors and rate limits
    """

    def __init__(self):
        """Initialize the Perplexity model with API credentials."""
        self.config = Config()
        self.api_key = self.config.get_api_key('perplexity')
        
        if not self.api_key:
            logger.warning("Perplexity API key not found. Perplexity functionality will be disabled.")
            return
            
        self.api_url = "https://api.perplexity.ai/chat/completions"
        self.model = "sonar"  # Updated to sonar model
        self.max_retries = 3
        self.retry_delay = 5  # seconds

    def generate_response(self, question: str) -> Optional[dict]:
        """
        Generate a response to a mathematical problem using Perplexity, including category prediction.
        
        Args:
            question: The mathematical problem to solve.
            
        Returns:
            A dictionary with the model's solution and predicted category, or None if an error occurs.
        """
        if not self.api_key:
            logger.error("Cannot generate response: Perplexity API key not configured")
            return None

        for attempt in range(self.max_retries):
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are an expert mathematical problem solver. Your task is to solve mathematical problems with precision and clarity.\n\nProblem-Solving Strategy:\n1. First, carefully read and understand the problem\n2. Identify the key mathematical concepts and formulas needed\n3. Break down the solution into clear, logical steps\n4. Show all calculations and intermediate results\n5. Verify your solution by checking each step\n6. Provide the final answer in a clear format\n\nGuidelines for Each Step:\n- Start with a clear understanding of what is being asked\n- List any relevant formulas or mathematical principles\n- Show your work in a step-by-step manner\n- Include units and labels where appropriate\n- Double-check all calculations\n- Verify your answer makes sense in the context of the problem\n- If you're unsure about any step, explain your reasoning\n\nRemember:\n- Accuracy is crucial - take your time to ensure each step is correct\n- Show all your work - don't skip steps\n- Use clear mathematical notation\n- End with a clear, boxed final answer\n\nAdditionally, after solving the problem, state the mathematical category of the problem (such as geometry, algebra, probability, sequences, or 'unknown' if you are not sure).\nFormat your answer as follows:\nSolution: <your step-by-step solution>\nCategory: <category name>"""
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    "max_tokens": 1000
                }
                response = requests.post(self.api_url, headers=headers, json=data)
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        retry_after = int(response.headers.get('Retry-After', self.retry_delay))
                        logger.info(f"Rate limit exceeded. Waiting {retry_after} seconds before retry...")
                        time.sleep(retry_after)
                        continue
                response.raise_for_status()
                content = response.json()['choices'][0]['message']['content'].strip()
                # Parse the response to extract solution and category
                solution = None
                category = None
                lines = content.split('\n')
                solution_lines = []
                for line in lines:
                    if line.strip().lower().startswith('category:'):
                        category = line.split(':', 1)[-1].strip()
                        break
                    else:
                        solution_lines.append(line)
                solution = '\n'.join(solution_lines).replace('Solution:', '').strip()
                return {'solution': solution, 'category': category}
            except requests.exceptions.RequestException as e:
                logger.error(f"Error generating Perplexity response: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                return None
            except Exception as e:
                logger.error(f"Unexpected error generating Perplexity response: {str(e)}")
                return None

# Example usage
if __name__ == "__main__":
    perplexity = PerplexityModel()
    response = perplexity.generate_response("How many stars are there in our galaxy?")
    print(response)