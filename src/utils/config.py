"""
Configuration Module for Mathematical Problem Evaluation System.

This module handles the loading and management of configuration settings,
including API keys and other environment variables. It provides functionality
to load configuration from environment variables and create template files.
"""

import os
from dotenv import load_dotenv
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Config:
    """
    Configuration manager for the application.
    
    This class provides methods to:
    - Load configuration from environment variables
    - Create template configuration files
    - Access configuration values
    """

    def __init__(self):
        """Initialize the configuration manager and load environment variables."""
        # Load environment variables from .env file
        load_dotenv()
        
        # Initialize configuration dictionary
        self.config = {
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'gemini_api_key': os.getenv('GEMINI_API_KEY'),
            'perplexity_api_key': os.getenv('PERPLEXITY_API_KEY')
        }
        
        # Validate configuration
        self._validate_config()

    def _validate_config(self) -> None:
        """
        Validate the configuration settings.
        
        Checks if all required API keys are present and logs warnings
        for any missing keys.
        """
        missing_keys = []
        for key, value in self.config.items():
            if not value:
                missing_keys.append(key)
        
        if missing_keys:
            logger.warning(f"Missing API keys: {', '.join(missing_keys)}")
            logger.warning("Some features may not work without these keys.")

    @staticmethod
    def create_env_template() -> None:
        """
        Create a template .env file with placeholder values.
        
        This method creates a .env file with placeholders for all required
        API keys if the file doesn't exist.
        """
        env_template = """# API Keys for Mathematical Problem Evaluation System

# OpenAI API Key (for ChatGPT)
OPENAI_API_KEY=your_openai_api_key_here

# Google API Key (for Gemini)
GEMINI_API_KEY=your_gemini_api_key_here

# Perplexity API Key
PERPLEXITY_API_KEY=your_perplexity_api_key_here
"""
        try:
            with open('.env', 'w') as f:
                f.write(env_template)
            logger.info("Created .env template file")
        except Exception as e:
            logger.error(f"Error creating .env template: {str(e)}")

    def get_api_key(self, service: str) -> str:
        """
        Get the API key for a specific service.
        
        Args:
            service: The name of the service (e.g., 'openai', 'gemini', 'perplexity').
            
        Returns:
            The API key for the specified service, or None if not found.
        """
        key_name = f"{service}_api_key"
        return self.config.get(key_name)

    def get_all_config(self) -> Dict[str, Any]:
        """
        Get all configuration values.
        
        Returns:
            Dictionary containing all configuration values.
        """
        return self.config.copy()

    def get_available_models(self) -> list:
        """Get list of available models based on API keys"""
        available_models = []
        
        if self.config['openai_api_key']:
            available_models.append("chatgpt")
        if self.config['gemini_api_key']:
            available_models.append("gemini")
        if self.config['perplexity_api_key']:
            available_models.append("perplexity")
            
        return available_models

    def is_model_available(self, model_name: str) -> bool:
        """Check if a specific model is available"""
        return model_name in self.get_available_models() 