"""
All command and message handlers for the bot
"""

import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import save_user, save_group, save_message, get_user, get_setting, set_setting
from utils import format_date, is_admin, get_user_mention

logger = logging.getLogger(__name__)

# ============================================
# COMMAND HANDLERS
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued"""
    user = update.effective_user
    
    # Save user to database
    save_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    # Save chat/group info if in group
    if update.effective_chat.type in ['group', 'supergroup']:
        save_group(
            group_id=update.effective_chat.id,
            group_name=update.effective_chat.title,
            group_type=update.effective_chat.type
        )
    
    welcome_text = f"""
👋 **Hello {user.first_name}!**

Welcome to **Group Assistant 344 Bot** 🤖

I'm here to help you manage your groups effectively and make your Telegram experience better!

---

**📌 Available Commands:**

🔹 `/start` - Show this welcome message
🔹 `/help` - Get help and support  
🔹 `/about` - Learn about this bot
🔹 `/ping` - Check if bot is alive
🔹 `/echo <message>` - Make me repeat after you
🔹 `/get_group_id` - Get current group ID
🔹 `/group_info` - Get group statistics
🔹 `/admin_help` - Show admin commands

---

**✨ Features:**
✅ Group Management
✅ User Statistics
✅ Message Handling
✅ 24/7 Availability
✅ Fast & Reliable

---

**📱 How to Add Me:**
1. Go to your group
2. Click on group name
3. Select "Add Members"
4. Search for @group_assistant344bot
5. Click "Add" 🎉

---

💡 _Type /help anytime for assistance!_
"""
    
    # Create inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("📚 Help", callback_data="help_menu"),
            InlineKeyboardButton("ℹ️ About", callback_data="about_menu")
        ],
        [
            InlineKeyboardButton("📊 Group Info", callback_data="group_info_menu"),
            InlineKeyboardButton("🔧 Admin", callback_data="admin_menu")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message"""
    help_text = """
📚 **Help & Support Guide**

---

**🔹 Basic Commands:**
• `/start` - Start the bot
• `/help` - Show this help message  
• `/about` - About this bot
• `/ping` - Check bot status
• `/echo <text>` - I'll repeat your message

---

**🔹 Group Management:**
• `/get_group_id` - Get group ID
• `/group_info` - Get group statistics
• `/admin_help` - Admin-only commands

---

**🔹 Admin Commands:**
• `/ban @username` - Ban a user
• `/unban @username` - Unban a user
• `/kick @username` - Kick a user
• `/promote @username` - Promote to admin
• `/demote @username` - Demote from admin

---

**📋 How to Add Me to Your Group:**

1. Open your group chat
2. Tap on group name at the top
3. Select **"Add Members"**
4. Search for `@group_assistant344bot`
5. Tap **"Add"** button

---

**⚠️ Important:**
For admin commands to work, I must be an **admin** in your group!

---

**🆘 Need More Help?**
Contact: @your_support_username
GitHub: https://github.com/your-username/your-repo

💡 _Type /start to see the welcome menu again_
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send information about the bot"""
    about_text = """
🤖 **About Group Assistant 344 Bot**

---

**Version:** 1.0.0
**Created:** July 2026
**Platform:** Telegram

---

**🚀 Features:**
• Group management utilities
• Advanced message handling
• User-friendly interface
• 24/7 availability
• Database storage
• Fast & reliable

---

**💻 Tech Stack:**
• Python 3.11
• python-telegram-bot v20+
• SQLite Database
• Deployed on Railway
• GitHub Integration

---

**📝 Open Source:**
🔗 GitHub: https://github.com/your-username/your-repo

---

**👨‍💻 Developer:**
Made with ❤️ by the Telegram Community

---

**📊 Statistics:**
• Uptime: 99.9%
• Users: Growing daily
• Groups: Active communities

---

💡 _Want to contribute? Check the GitHub repository!_
"""
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if the bot is alive"""
    start_time = datetime.now()
    await update.message.reply_text("🏓 Pinging...")
    
    # Calculate response time
    end_time = datetime.now()
    response_time = (end_time - start_time).total_seconds() * 1000
    
    await update.message.reply_text(
        f"✅ **Pong!** I'm alive and kicking!\n"
        f"⏱️ Response time: `{response_time:.0f}ms`\n"
        f"🕐 Server time: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        parse_mode='Markdown'
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user's message"""
    if context.args:
        echo_text = ' '.join(context.args)
        await update.message.reply_text(f"🔊 **You said:**\n{echo_text}", parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "⚠️ **Please provide a message to echo.**\n"
            "Example: `/echo Hello World!`",
            parse_mode='Markdown'
        )

async def get_group_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get the current chat/group ID"""
    chat = update.effective_chat
    chat_id = chat.id
    chat_type = chat.type
    chat_title = chat.title or "Private Chat"
    
    # Save group info
    if chat_type in ['group', 'supergroup']:
        save_group(chat_id, chat_title, chat_type)
    
    message = f"""
📊 **Chat Information**

📌 **Title:** {chat_title}
🆔 **ID:** `{chat_id}`
📝 **Type:** {chat_type}

---

⚠️ **Important:**
• Keep this ID secure!
• Used for admin commands
• Unique identifier for this chat

---

💡 **Pro Tip:** Use this ID in /group_info to get detailed statistics
"""
    await update.message.reply_text(message, parse_mode='Markdown')

async def group_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get detailed information about the group"""
    chat = update.effective_chat
    
    if chat.type in ['group', 'supergroup']:
        try:
            # Get member count
            member_count = await context.bot.get_chat_member_count(chat.id)
            
            # Save group info
            save_group(chat.id, chat.title, chat.type)
            
            # Get bot's admin status
            bot_member = await context.bot.get_chat_member(chat.id, context.bot.id)
            is_admin = bot_member.status in ['administrator', 'creator']
            
            info_text = f"""
📊 **Group Statistics**

---

📌 **Name:** {chat.title}
🆔 **ID:** `{chat.id}`
👥 **Members:** {member_count}
📝 **Type:** {chat.type}

🔗 **Link:** {chat.invite_link or 'Not available'}

---

**🤖 Bot Status:**
• Admin: {'✅ Yes' if is_admin else '❌ No'}
• Status: {'✅ Active' if is_admin else '⚠️ Limited'}

---

**ℹ️ Information:**
• Created: {format_date(chat.date) if hasattr(chat, 'date') else 'Unknown'}
• Language: {chat.language_code or 'Not specified'}

---

💡 _For admin features, make me an admin in your group!_
"""
            await update.message.reply_text(info_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error getting group info: {str(e)}")
            await update.message.reply_text(
                "⚠️ **Error:** Could not get group information.\n"
                "Make sure I'm an admin in the group!",
                parse_mode='Markdown'
            )
    else:
        await update.message.reply_text(
            "⚠️ **This command only works in groups!**\n"
            "Please add me to a group and try again.",
            parse_mode='Markdown'
        )

async def admin_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show admin-only commands"""
    # Check if user is admin in the group
    if update.effective_chat.type in ['group', 'supergroup']:
        user_member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        is_admin = user_member.status in ['administrator', 'creator']
        
        if not is_admin:
            await update.message.reply_text(
                "⚠️ **Access Denied!**\n"
                "You need to be an admin to view these commands.",
                parse_mode='Markdown'
            )
            return
    
    admin_text = """
🔐 **Admin Commands Guide**

---

**📋 Available Commands:**

🛑 `/ban @username` - Ban a user from the group
✅ `/unban @username` - Unban a previously banned user
🚫 `/kick @username` - Kick a user from the group
⬆️ `/promote @username` - Promote user to admin
⬇️ `/demote @username` - Demote admin to regular user

---

**⚙️ Requirements:**

1. **I must be an admin** in your group
2. You must have admin privileges
3. The user must be in the group

---

**🛡️ Permissions Needed:**
• Ban users: ✅
• Delete messages: ✅
• Add new members: ✅
• Change group info: ✅

---

**💡 Pro Tips:**
• Use `/get_group_id` to get group ID
• Use `/group_info` for statistics
• Use @username or user ID

---

⚠️ **Warning:** Use these commands responsibly!
"""
    await update.message.reply_text(admin_text, parse_mode='Markdown')

# ============================================
# MESSAGE HANDLERS
# ============================================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages"""
    user = update.effective_user
    message = update.message
    text = message.text
    
    # Save message to database
    save_user(user.id, user.username, user.first_name, user.last_name)
    
    if update.effective_chat.type in ['group', 'supergroup']:
        save_group(update.effective_chat.id, update.effective_chat.title, update.effective_chat.type)
        save_message(user.id, update.effective_chat.id, text)
    
    # Log the message
    logger.info(f"💬 {user.first_name} (@{user.username}): {text[:50]}...")
    
    # Auto-reply for specific keywords
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        await update.message.reply_text(
            f"👋 **Hello {user.first_name}!**\n"
            f"How can I assist you today?\n"
            f"Type `/help` to see available commands.",
            parse_mode='Markdown'
        )
    
    elif any(word in text_lower for word in ['thanks', 'thank you', 'thx']):
        await update.message.reply_text(
            f"😊 **You're welcome {user.first_name}!**\n"
            f"Happy to help! 🙌"
        )
    
    elif any(word in text_lower for word in ['bye', 'goodbye', 'see you']):
        await update.message.reply_text(
            f"👋 **Goodbye {user.first_name}!**\n"
            f"See you later! 🌟"
        )
    
    elif any(word in text_lower for word in ['bot', 'assistant']):
        await update.message.reply_text(
            f"🤖 **Yes, I'm here {user.first_name}!**\n"
            f"I'm Group Assistant 344, your AI helper.\n"
            f"Type `/help` to see what I can do! 💪"
        )

# ============================================
# CALLBACK QUERY HANDLERS
# ============================================

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button presses"""
    query = update.callback_query
    user = query.from_user
    data = query.data
    
    await query.answer()
    
    if data == "help_menu":
        await query.edit_message_text(
            "📚 **Help Menu**\n\n"
            "Type `/help` for full command list!\n"
            "Add me to your group for group management features.",
            parse_mode='Markdown'
        )
    
    elif data == "about_menu":
        await query.edit_message_text(
            "🤖 **Group Assistant 344 Bot**\n\n"
            "Version: 1.0.0\n"
            "Creator: @your_username\n"
            "GitHub: https://github.com/your-username/your-repo\n\n"
            "Made with ❤️ for the Telegram community!",
            parse_mode='Markdown'
        )
    
    elif data == "group_info_menu":
        await query.edit_message_text(
            "📊 **Group Info**\n\n"
            "Type `/get_group_id` to see group ID\n"
            "Type `/group_info` for detailed statistics\n\n"
            "Make me admin for full features!",
            parse_mode='Markdown'
        )
    
    elif data == "admin_menu":
        await query.edit_message_text(
            "🔧 **Admin Menu**\n\n"
            "Type `/admin_help` for all admin commands\n\n"
            "**Requirements:**\n"
            "• I must be an admin\n"
            "• You must have admin rights\n\n"
            "⚠️ Use responsibly!",
            parse_mode='Markdown'
        )
    
    else:
        await query.edit_message_text(
            f"⚠️ Unknown option: {data}\n"
            f"Try the main menu with `/start`",
            parse_mode='Markdown'
        )

# ============================================
# ERROR HANDLER
# ============================================

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"❌ Update {update} caused error: {context.error}")
    
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "⚠️ **Oops! Something went wrong.**\n\n"
                "Please try again later.\n"
                "If the problem persists, contact support.",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"❌ Could not send error message: {str(e)}")
