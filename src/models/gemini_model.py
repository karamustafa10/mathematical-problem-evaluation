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

    def generate_response(self, question: str) -> Optional[dict]:
        """
        Generate a response to a mathematical problem using Gemini, including category prediction.
        
        Args:
            question: The mathematical problem to solve.
            
        Returns:
            A dictionary with the model's solution and predicted category, or None if an error occurs.
        """
        if not self.api_key:
            logger.error("Cannot generate response: Gemini API key not configured")
            return None
            
        if not self.model:
            logger.error("Cannot generate response: Gemini model not initialized")
            return None

        for attempt in range(self.max_retries):
            try:
                generation_config = {
                    "temperature": 0.3,
                    "top_p": 0.8,
                    "top_k": 40,
                    "max_output_tokens": 1000,
                }
                prompt = f"""You are an expert mathematical problem solver. Your task is to solve mathematical problems with precision and clarity.\n\nProblem: {question}\n\nProblem-Solving Strategy:\n1. First, carefully read and understand the problem\n2. Identify the key mathematical concepts and formulas needed\n3. Break down the solution into clear, logical steps\n4. Show all calculations and intermediate results\n5. Verify your solution by checking each step\n6. Provide the final answer in a clear format\n\nGuidelines for Each Step:\n- Start with a clear understanding of what is being asked\n- List any relevant formulas or mathematical principles\n- Show your work in a step-by-step manner\n- Include units and labels where appropriate\n- Double-check all calculations\n- Verify your answer makes sense in the context of the problem\n- If you're unsure about any step, explain your reasoning\n\nRemember:\n- Accuracy is crucial - take your time to ensure each step is correct\n- Show all your work - don't skip steps\n- Use clear mathematical notation\n- End with a clear, boxed final answer\n\nAdditionally, after solving the problem, state the mathematical category of the problem (such as geometry, algebra, probability, sequences, or 'unknown' if you are not sure).\nFormat your answer as follows:\nSolution: <your step-by-step solution>\nCategory: <category name>"""
                response = self.model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                content = response.text.strip()
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
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Error generating Gemini response: {error_msg}")
                if "API_KEY_INVALID" in error_msg or "API key expired" in error_msg:
                    logger.error("Gemini API key is invalid or expired. Please update your API key.")
                    return None
                if "429" in error_msg and "quota" in error_msg.lower():
                    if attempt < self.max_retries - 1:
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