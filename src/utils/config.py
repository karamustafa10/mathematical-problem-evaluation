import os
from typing import Optional
from dotenv import load_dotenv

class Config:
    def __init__(self):
        # Load environment variables from .env file if it exists
        load_dotenv()
        
        # API Keys
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')
        
        # Model Settings
        self.chatgpt_model = "gpt-3.5-turbo"
        self.gemini_model = "gemini-pro"
        self.perplexity_model = "pplx-7b-online"
        
        # Directory Settings
        self.data_dir = "data"
        self.results_dir = "results"
        
        # Create necessary directories
        self._create_directories()
        
        # Validate configuration
        self._validate_config()

    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)

    def _validate_config(self):
        """Validate the configuration settings"""
        # Check if at least one API key is available
        if not any([self.openai_api_key, self.google_api_key, self.perplexity_api_key]):
            print("Warning: No API keys found. Please set at least one of the following environment variables:")
            print("- OPENAI_API_KEY")
            print("- GOOGLE_API_KEY")
            print("- PERPLEXITY_API_KEY")
            print("\nYou can set these in a .env file in the project root directory.")

    def get_available_models(self) -> list:
        """Get list of available models based on API keys"""
        available_models = []
        
        if self.openai_api_key:
            available_models.append("chatgpt")
        if self.google_api_key:
            available_models.append("gemini")
        if self.perplexity_api_key:
            available_models.append("perplexity")
            
        return available_models

    def is_model_available(self, model_name: str) -> bool:
        """Check if a specific model is available"""
        return model_name in self.get_available_models()

    @staticmethod
    def create_env_template():
        """Create a template .env file"""
        template = """# API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# Optional Settings
# CHATGPT_MODEL=gpt-3.5-turbo
# GEMINI_MODEL=gemini-pro
# PERPLEXITY_MODEL=pplx-7b-online
"""
        with open('.env.template', 'w') as f:
            f.write(template)
        print("Created .env.template file. Please copy it to .env and add your API keys.") 