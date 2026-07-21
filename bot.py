import os
import logging

# Simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get token
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN not set!")
    exit(1)

logger.info(f"✅ Token: {TOKEN[:10]}...")

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler
except ImportError:
    logger.error("❌ telegram module not installed")
    exit(1)

async def start(update, context):
    await update.message.reply_text("Hello! I'm working! 🎉")

def main():
    logger.info("🚀 Starting bot...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    logger.info("✅ Bot is running!")
    app.run_polling()

if __name__ == "__main__":
    main()
