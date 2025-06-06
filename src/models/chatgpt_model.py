import os
from openai import OpenAI
from typing import Optional

class ChatGPTModel:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-3.5-turbo"

    def generate_response(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Generate a response using ChatGPT
        
        Args:
            prompt (str): The input prompt
            system_message (str, optional): System message to guide the model
            
        Returns:
            str: Model's response
        """
        try:
            if system_message is None:
                system_message = (
                    "You are a mathematical problem solver. "
                    "Please solve the problem step by step, showing your work and reasoning. "
                    "Make sure to clearly indicate each step of your solution process."
                )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content

        except Exception as e:
            error_message = f"Error in ChatGPT API call: {str(e)}"
            print(error_message)
            return f"Error: {error_message}"

# Example usage
if __name__ == "__main__":
    chatgpt = ChatGPTModel()
    response = chatgpt.generate_response("Tell me a three sentence bedtime story about a unicorn.")
    print(response)
