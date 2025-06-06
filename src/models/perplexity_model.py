import os
import requests
from typing import Optional
import logging

class PerplexityModel:
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY environment variable is not set")
        
        self.api_url = "https://api.perplexity.ai/chat/completions"
        self.model = "sonar"  # Using the correct model name from documentation

    def generate_response(self, prompt: str, system_message: str = None) -> Optional[str]:
        """
        Generate a response using the Perplexity API
        
        Args:
            prompt (str): The problem prompt
            system_message (str, optional): System message to guide the model
            
        Returns:
            Optional[str]: The model's response or None if an error occurs
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": self.model,
                "messages": messages
            }
            
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            if "choices" not in result or not result["choices"]:
                logging.error("Unexpected response format from Perplexity API")
                return "Error: Unexpected response format"
                
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error in Perplexity API call: {str(e)}")
            return f"Error: {str(e)}"
        except Exception as e:
            logging.error(f"Unexpected error in Perplexity API call: {str(e)}")
            return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    perplexity = PerplexityModel()
    response = perplexity.generate_response("How many stars are there in our galaxy?")
    print(response)