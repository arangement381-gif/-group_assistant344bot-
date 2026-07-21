import os
import sys
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN is not set!")
    logger.info("Please set TELEGRAM_BOT_TOKEN in Railway variables")
    sys.exit(1)

logger.info(f"✅ Token loaded: {TOKEN[:10]}...")

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
except ImportError as e:
    logger.error(f"❌ Failed to import telegram: {e}")
    sys.exit(1)

# Simple handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working! Group Assistant 344 is online!")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong!")

def main():
    try:
        logger.info("🚀 Starting bot...")
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("ping", ping))
        logger.info("✅ Bot is running!")
        app.run_polling()
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
