import os
import logging
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import Update
from config import Config
from handlers import (
    start, help_command, about, ping, echo, 
    get_group_id, group_info, admin_help, 
    handle_text, handle_callback, error_handler
)
from database import init_db

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main function to start the bot"""
    try:
        # Initialize database
        init_db()
        logger.info("✅ Database initialized successfully")
        
        # Get bot token - with better error handling
        token = os.environ.get('TELEGRAM_BOT_TOKEN')
        
        if not token or token == "YOUR_BOT_TOKEN_HERE":
            logger.error("❌ TELEGRAM_BOT_TOKEN is missing or invalid")
            logger.error("Please set TELEGRAM_BOT_TOKEN in Railway environment variables")
            logger.info("To fix this:")
            logger.info("1. Go to your Railway project")
            logger.info("2. Click on your service")
            logger.info("3. Go to the 'Variables' tab")
            logger.info("4. Add TELEGRAM_BOT_TOKEN with your bot token")
            logger.info("5. Redeploy the service")
            sys.exit(1)
        
        # Create application
        application = Application.builder().token(token).build()
        logger.info("✅ Bot application created successfully")
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about))
        application.add_handler(CommandHandler("ping", ping))
        application.add_handler(CommandHandler("echo", echo))
        application.add_handler(CommandHandler("get_group_id", get_group_id))
        application.add_handler(CommandHandler("group_info", group_info))
        application.add_handler(CommandHandler("admin_help", admin_help))
        
        # Add message handler for regular text
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        # Add callback query handler for inline buttons
        application.add_handler(CallbackQueryHandler(handle_callback))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        # Start the bot (polling for Railway)
        logger.info("🚀 Bot is starting and polling for updates...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {str(e)}")
        logger.info("Attempting to restart in 5 seconds...")
        import time
        time.sleep(5)
        sys.exit(1)

if __name__ == "__main__":
    main()
