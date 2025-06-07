"""
ChatGPT Model Module for Mathematical Problem Evaluation System.

This module provides an interface to interact with OpenAI's ChatGPT model
for solving mathematical problems. It handles API communication, response
generation, and error handling.
"""

from openai import OpenAI
import logging
from typing import Optional
from utils.config import Config

logger = logging.getLogger(__name__)

class ChatGPTModel:
    """
    Interface for interacting with OpenAI's ChatGPT model.
    
    This class provides methods to:
    - Initialize the ChatGPT model with API credentials
    - Generate responses to mathematical problems
    - Handle API errors and rate limits
    """

    def __init__(self):
        """Initialize the ChatGPT model with API credentials."""
        self.config = Config()
        self.api_key = self.config.get_api_key('openai')
        
        if not self.api_key:
            logger.warning("OpenAI API key not found. ChatGPT functionality will be disabled.")
            return
            
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"

    def generate_response(self, question: str) -> Optional[str]:
        """
        Generate a response to a mathematical problem using ChatGPT.
        
        Args:
            question: The mathematical problem to solve.
            
        Returns:
            The model's response as a string, or None if an error occurs.
        """
        if not self.api_key:
            logger.error("Cannot generate response: OpenAI API key not configured")
            return None

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": """You are an expert mathematical problem solver. Your task is to solve mathematical problems with precision and clarity.

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
- End with a clear, boxed final answer"""},
                    {"role": "user", "content": question}
                ],
                temperature=0.3,  # Lower temperature for more focused responses
                max_tokens=1000  # Increased token limit for more detailed solutions
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating ChatGPT response: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    chatgpt = ChatGPTModel()
    response = chatgpt.generate_response("Tell me a three sentence bedtime story about a unicorn.")
    print(response)
