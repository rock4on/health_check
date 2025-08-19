"""OpenAI configuration settings."""
import os
from typing import Optional


class OpenAIConfig:
    """Configuration for OpenAI API."""
    
    def __init__(self):
        """Initialize configuration."""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.1'))
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '2000'))
    
    def get_api_key(self) -> Optional[str]:
        """Get API key from environment or return None."""
        return self.api_key
    
    def get_base_url(self) -> str:
        """Get base URL for OpenAI API."""
        return self.base_url
    
    def validate(self) -> bool:
        """Validate that required configuration is present."""
        return self.api_key is not None