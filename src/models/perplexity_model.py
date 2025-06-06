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
        self.model = "pplx-7b-online"

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
                        "content": "You are a mathematical problem solver. "
                                 "Provide clear, step-by-step solutions and "
                                 "end with the final answer."
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "temperature": 0.3,  # Lower temperature for more focused responses
                "max_tokens": 500
            }
            
            # Make the API request
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Extract and return the response text
            return response.json()['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            logger.error(f"Error generating Perplexity response: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    perplexity = PerplexityModel()
    response = perplexity.generate_response("How many stars are there in our galaxy?")
    print(response)