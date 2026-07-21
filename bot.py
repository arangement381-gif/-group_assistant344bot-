import os
import logging
import sys

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get token
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN not set!")
    sys.exit(1)

logger.info(f"✅ Token found: {TOKEN[:10]}...")

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
except ImportError as e:
    logger.error(f"❌ Failed to import telegram: {e}")
    sys.exit(1)

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n"
        f"I'm Group Assistant 344 Bot 🤖\n"
        f"Type /help for commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Commands:\n"
        "/start - Welcome\n"
        "/help - This help\n"
        "/ping - Check alive\n"
        "/echo <text> - Repeat\n"
        "/get_group_id - Group ID\n"
        "/group_info - Group stats"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await update.message.reply_text(' '.join(context.args))
    else:
        await update.message.reply_text("Usage: /echo <message>")

async def get_group_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Group ID: `{update.effective_chat.id}`", parse_mode='Markdown')

async def group_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ['group', 'supergroup']:
        try:
            count = await context.bot.get_chat_member_count(chat.id)
            await update.message.reply_text(
                f"📊 {chat.title}\n"
                f"Members: {count}\n"
                f"Type: {chat.type}"
            )
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
    else:
        await update.message.reply_text("This command only works in groups!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = update.effective_user
    
    if text in ['hello', 'hi', 'hey']:
        await update.message.reply_text(f"👋 Hi {user.first_name}!")
    elif text in ['thanks', 'thank you', 'thx']:
        await update.message.reply_text(f"😊 Welcome {user.first_name}!")

def main():
    try:
        logger.info("🚀 Starting bot...")
        
        # Create application
        app = Application.builder().token(TOKEN).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("ping", ping))
        app.add_handler(CommandHandler("echo", echo))
        app.add_handler(CommandHandler("get_group_id", get_group_id))
        app.add_handler(CommandHandler("group_info", group_info))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        logger.info("✅ Bot ready! Starting polling...")
        app.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
