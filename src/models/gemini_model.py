import os
import google.generativeai as genai
from typing import Optional
import logging

class GeminiModel:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        
        genai.configure(api_key=api_key)
        # List available models
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Available model: {m.name}")
        
        self.model = genai.GenerativeModel('gemini-1.5-flash')  # Using flash model which should be in free tier

    def generate_response(self, prompt: str, system_message: str = None) -> Optional[str]:
        """
        Generate a response using the Gemini model
        
        Args:
            prompt (str): The problem prompt
            system_message (str, optional): System message to guide the model
            
        Returns:
            Optional[str]: The model's response or None if an error occurs
        """
        try:
            if system_message is None:
                system_message = (
                    "You are a mathematical problem solver. "
                    "Please solve the problem step by step, showing your work and reasoning. "
                    "Make sure to clearly indicate each step of your solution process."
                )

            # Combine system message and prompt
            full_prompt = f"{system_message}\n\n{prompt}" if system_message else prompt
            
            response = self.model.generate_content(full_prompt)
            
            if not response.text:
                logging.error("Empty response from Gemini API")
                return "Error: Empty response from model"
                
            return response.text
            
        except Exception as e:
            logging.error(f"Error in Gemini API call: {str(e)}")
            return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    gemini = GeminiModel()
    response = gemini.generate_response("Explain how AI works in a few words")
    print(response)