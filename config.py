import os
from dotenv import load_dotenv

# Load environment variables from .env file (local development only)
load_dotenv()

class Config:
    """Bot configuration class"""
    
    # Required: Telegram Bot Token (from @BotFather)
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    # If token is missing, use a placeholder (for development only)
    if not TELEGRAM_BOT_TOKEN:
        print("⚠️ WARNING: TELEGRAM_BOT_TOKEN not set. Using placeholder.")
        TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    
    # Optional: Bot settings
    BOT_NAME = os.environ.get('BOT_NAME', 'Group Assistant 344')
    BOT_USERNAME = os.environ.get('BOT_USERNAME', 'group_assistant344bot')
    
    # Database settings
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///bot_data.db')
    
    # Admin user IDs (comma-separated list)
    ADMIN_IDS = [int(id.strip()) for id in os.environ.get('ADMIN_IDS', '').split(',') if id.strip()]
    
    # Webhook settings (for future use)
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL', None)
    WEBHOOK_PORT = int(os.environ.get('PORT', 8080))
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        return True
