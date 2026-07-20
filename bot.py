import os
import telebot
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    logger.error("BOT_TOKEN environment variable not set!")
    raise ValueError("BOT_TOKEN is required")

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# ============ BOT COMMAND HANDLERS ============

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handle /start and /help commands"""
    user_id = message.from_user.id
    username = message.from_user.username or "User"
    
    welcome_text = (
        f"👋 Hello {username}!\n\n"
        "I'm an Echo Bot. Send me any text, and I'll repeat it back to you.\n\n"
        "📌 Try these:\n"
        "- Send any message to echo it\n"
        "- Send /help to see this message again\n"
        "- Send /about to learn more\n"
        "- Send /ping to check latency\n\n"
        "Simple, fast, and always here! 🚀"
    )
    
    bot.reply_to(message, welcome_text)
    logger.info(f"User {user_id} ({username}) started the bot")

@bot.message_handler(commands=['about'])
def send_about(message):
    """Handle /about command"""
    about_text = (
        "🤖 About Echo Bot\n\n"
        "This bot is a simple echo bot designed for Telegram Ads.\n"
        "It's fast, reliable, and always ready to respond.\n\n"
        "💡 Features:\n"
        "- Instant message echoing\n"
        "- 24/7 availability\n"
        "- Clean and simple interface\n\n"
        "📱 Built with ❤️ using Python"
    )
    bot.reply_to(message, about_text)
    logger.info(f"User {message.from_user.id} requested about info")

@bot.message_handler(commands=['ping'])
def send_ping(message):
    """Handle /ping command to test bot responsiveness"""
    start_time = time.time()
    response = bot.reply_to(message, "🏓 Pong!")
    end_time = time.time()
    
    latency = round((end_time - start_time) * 1000, 2)
    bot.edit_message_text(
        f"🏓 Pong! (Response time: {latency}ms)",
        chat_id=message.chat.id,
        message_id=response.message_id
    )

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    """Echo back any other message"""
    user_id = message.from_user.id
    
    # Echo the message
    bot.reply_to(message, message.text)
    logger.info(f"Echoed message from user {user_id}: {message.text[:50]}")

# ============ MAIN ENTRY POINT ============

if __name__ == '__main__':
    logger.info("Starting Echo Bot in POLLING mode...")
    logger.info(f"Bot username: @{bot.get_me().username}")
    logger.info("Bot is ready! Press Ctrl+C to stop.")
    
    try:
        # Start polling (this is more reliable for simple bots)
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        raise
