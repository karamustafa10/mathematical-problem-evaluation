"""
Gemini Model Module for Mathematical Problem Evaluation System.

This module provides an interface to interact with Google's Gemini model
for solving mathematical problems. It handles API communication, response
generation, and error handling.
"""

import os
import google.generativeai as genai
from typing import Optional
import logging
from utils.config import Config

logger = logging.getLogger(__name__)

class GeminiModel:
    """
    Interface for interacting with Google's Gemini model.
    
    This class provides methods to:
    - Initialize the Gemini model with API credentials
    - Generate responses to mathematical problems
    - Handle API errors and rate limits
    """

    def __init__(self):
        """Initialize the Gemini model with API credentials."""
        self.config = Config()
        self.api_key = self.config.get_api_key('gemini')
        
        if not self.api_key:
            logger.warning("Gemini API key not found. Gemini functionality will be disabled.")
            return
            
        genai.configure(api_key=self.api_key)
        # List available models
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Available model: {m.name}")
        
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_response(self, question: str) -> Optional[str]:
        """
        Generate a response to a mathematical problem using Gemini.
        
        Args:
            question: The mathematical problem to solve.
            
        Returns:
            The model's response as a string, or None if an error occurs.
        """
        if not self.api_key:
            logger.error("Cannot generate response: Gemini API key not configured")
            return None

        try:
            # Configure the model for mathematical problem solving
            generation_config = {
                "temperature": 0.3,  # Lower temperature for more focused responses
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 500,
            }
            
            # Create the prompt with system instructions
            prompt = f"""You are a mathematical problem solver. Please solve the following problem step by step.
            Show your work and reasoning clearly. End with the final answer.

            Problem: {question}"""
            
            # Generate the response
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error generating Gemini response: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    gemini = GeminiModel()
    response = gemini.generate_response("Explain how AI works in a few words")
    print(response)