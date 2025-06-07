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

    def generate_response(self, question: str) -> Optional[str]:
        """
        Generate a response to a mathematical problem using Perplexity.
        
        Args:
            question: The mathematical problem to solve.
            
        Returns:
            The model's response as a string, or None if an error occurs.
        """
        if not self.api_key:
            logger.error("Cannot generate response: Perplexity API key not configured")
            return None

        for attempt in range(self.max_retries):
            try:
                # Prepare the API request
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are an expert mathematical problem solver. Your task is to solve mathematical problems with precision and clarity.

Problem-Solving Strategy:
1. First, carefully read and understand the problem
2. Identify the key mathematical concepts and formulas needed
3. Break down the solution into clear, logical steps
4. Show all calculations and intermediate results
5. Verify your solution by checking each step
6. Provide the final answer in a clear format

Guidelines for Each Step:
- Start with a clear understanding of what is being asked
- List any relevant formulas or mathematical principles
- Show your work in a step-by-step manner
- Include units and labels where appropriate
- Double-check all calculations
- Verify your answer makes sense in the context of the problem
- If you're unsure about any step, explain your reasoning

Remember:
- Accuracy is crucial - take your time to ensure each step is correct
- Show all your work - don't skip steps
- Use clear mathematical notation
- End with a clear, boxed final answer"""
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    "max_tokens": 1000  # Increased token limit for more detailed solutions
                }
                
                # Make the API request
                response = requests.post(self.api_url, headers=headers, json=data)
                
                # Check for rate limiting
                if response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        retry_after = int(response.headers.get('Retry-After', self.retry_delay))
                        logger.info(f"Rate limit exceeded. Waiting {retry_after} seconds before retry...")
                        time.sleep(retry_after)
                        continue
                
                # Raise an exception for other error status codes
                response.raise_for_status()
                
                # Extract and return the response text
                return response.json()['choices'][0]['message']['content'].strip()
                
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