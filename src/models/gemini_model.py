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
import time
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
            
        try:
            genai.configure(api_key=self.api_key)
            # List available models
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"Available model: {m.name}")
            
            # Use gemini-2.0-flash model
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.max_retries = 3
            self.retry_delay = 5  # seconds
            
        except Exception as e:
            logger.error(f"Error initializing Gemini model: {str(e)}")
            self.model = None

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
            
        if not self.model:
            logger.error("Cannot generate response: Gemini model not initialized")
            return None

        for attempt in range(self.max_retries):
            try:
                # Configure the model for mathematical problem solving
                generation_config = {
                    "temperature": 0.3,  # Lower temperature for more focused responses
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 1000,  # Increased token limit for more detailed solutions
                }
                
                # Create the prompt with system instructions
                prompt = f"""You are an expert mathematical problem solver. Your task is to solve mathematical problems with precision and clarity.

Problem: {question}

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
                
                # Generate the response
                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                
                return response.text.strip()
                
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Error generating Gemini response: {error_msg}")
                
                # Check for API key errors
                if "API_KEY_INVALID" in error_msg or "API key expired" in error_msg:
                    logger.error("Gemini API key is invalid or expired. Please update your API key.")
                    return None
                
                # Check if it's a rate limit error
                if "429" in error_msg and "quota" in error_msg.lower():
                    if attempt < self.max_retries - 1:
                        # Extract retry delay from error message if available
                        try:
                            import re
                            delay_match = re.search(r'retry_delay\s*{\s*seconds:\s*(\d+)', error_msg)
                            if delay_match:
                                retry_delay = int(delay_match.group(1))
                            else:
                                retry_delay = self.retry_delay * (attempt + 1)
                        except:
                            retry_delay = self.retry_delay * (attempt + 1)
                            
                        logger.info(f"Rate limit exceeded. Waiting {retry_delay} seconds before retry...")
                        time.sleep(retry_delay)
                        continue
                
                return None

# Example usage
if __name__ == "__main__":
    gemini = GeminiModel()
    response = gemini.generate_response("Explain how AI works in a few words")
    print(response)