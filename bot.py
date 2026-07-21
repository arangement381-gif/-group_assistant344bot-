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
    sys.exit(1)

logger.info(f"✅ Token loaded: {TOKEN[:10]}...")

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
except ImportError as e:
    logger.error(f"❌ Failed to import telegram: {e}")
    sys.exit(1)

# ===== COMMAND HANDLERS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n"
        f"✅ Bot is working! Group Assistant 344 is online!\n\n"
        f"Commands:\n"
        f"/start - Welcome message\n"
        f"/ping - Check if I'm alive\n"
        f"/help - Show all commands\n"
        f"/echo <text> - Repeat your message\n\n"
        f"💡 Just type 'hello' or 'hi' and I'll reply!"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ping command"""
    await update.message.reply_text("🏓 Pong! I'm alive!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    await update.message.reply_text(
        "📚 Commands:\n"
        "/start - Welcome\n"
        "/ping - Check alive\n"
        "/help - This help\n"
        "/echo <text> - Repeat message\n\n"
        "💡 Type 'hello' or 'hi' for auto-reply!"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo command"""
    if context.args:
        await update.message.reply_text(' '.join(context.args))
    else:
        await update.message.reply_text("Usage: /echo <message>")

async def get_group_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get group ID"""
    await update.message.reply_text(f"Group ID: `{update.effective_chat.id}`", parse_mode='Markdown')

async def group_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Group info"""
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

# ===== TEXT MESSAGE HANDLER (This is what you're missing!) =====

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages"""
    text = update.message.text.lower()
    user = update.effective_user
    
    logger.info(f"📩 Received: '{text}' from {user.first_name}")
    
    # Auto-reply to specific messages
    if text in ['hello', 'hi', 'hey', 'greetings']:
        await update.message.reply_text(f"👋 Hi {user.first_name}! How can I help?")
    
    elif text in ['thanks', 'thank you', 'thx']:
        await update.message.reply_text(f"😊 You're welcome {user.first_name}!")
    
    elif text in ['bye', 'goodbye']:
        await update.message.reply_text(f"👋 See you later {user.first_name}!")
    
    elif 'welcome' in text:
        await update.message.reply_text(f"🎉 Welcome {user.first_name}! Glad to have you here!")
    
    elif 'how are you' in text:
        await update.message.reply_text(f"🤖 I'm great {user.first_name}! Thanks for asking!")
    
    elif 'what is your name' in text:
        await update.message.reply_text(f"🤖 I'm Group Assistant 344 Bot! Nice to meet you {user.first_name}!")
    
    elif 'who are you' in text:
        await update.message.reply_text(f"🤖 I'm a Telegram bot created to help manage groups!")
    
    elif 'what can you do' in text:
        await update.message.reply_text(
            f"💪 I can:\n"
            f"• Reply to messages\n"
            f"• Show group info\n"
            f"• Echo messages\n"
            f"• And more!\n\n"
            f"Type /help to see all commands!"
        )
    
    else:
        # Default response for unknown messages
        await update.message.reply_text(
            f"💬 I heard you say: '{text}'\n\n"
            f"Type /help to see what I can do!\n"
            f"Or try saying 'hello' or 'hi'!"
        )

# ===== MAIN FUNCTION =====

def main():
    try:
        logger.info("🚀 Starting bot...")
        
        # Create application
        app = Application.builder().token(TOKEN).build()
        
        # Add command handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("ping", ping))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("echo", echo))
        app.add_handler(CommandHandler("get_group_id", get_group_id))
        app.add_handler(CommandHandler("group_info", group_info))
        
        # Add text message handler (THIS IS KEY!)
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        logger.info("✅ Bot is ready! Starting polling...")
        app.run_polling()
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
