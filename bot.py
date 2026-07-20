import os
import telebot
from flask import Flask, request
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app for webhook
app = Flask(__name__)

# Get bot token from environment variable
TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    logger.error("BOT_TOKEN environment variable not set!")
    raise ValueError("BOT_TOKEN is required")

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Store user activity for analytics (simple tracking)
user_activity = {}

# ============ BOT COMMAND HANDLERS ============

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handle /start and /help commands"""
    user_id = message.from_user.id
    username = message.from_user.username or "User"
    
    # Track user activity
    user_activity[user_id] = {
        'last_active': datetime.now().isoformat(),
        'username': username
    }
    
    welcome_text = (
        f"👋 Hello {username}!\n\n"
        "I'm an Echo Bot. Send me any text, and I'll repeat it back to you.\n\n"
        "📌 Try these:\n"
        "- Send any message to echo it\n"
        "- Send /help to see this message again\n"
        "- Send /about to learn more\n\n"
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
        "📱 Built with ❤️ using Python and Flask"
    )
    bot.reply_to(message, about_text)
    logger.info(f"User {message.from_user.id} requested about info")

@bot.message_handler(commands=['ping'])
def send_ping(message):
    """Handle /ping command to test bot responsiveness"""
    start_time = time.time()
    response = bot.reply_to(message, "🏓 Pong!")
    end_time = time.time()
    
    # Edit the response to show latency
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
    
    # Track user activity
    user_activity[user_id] = {
        'last_active': datetime.now().isoformat(),
        'username': message.from_user.username or "User"
    }
    
    # Echo the message
    bot.reply_to(message, message.text)
    logger.info(f"Echoed message from user {user_id}: {message.text[:50]}")

# ============ WEBHOOK SETUP FOR RAILWAY ============

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook requests from Telegram"""
    try:
        # Get the update data
        update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
        if update:
            # Process the update
            bot.process_new_updates([update])
            logger.info("Webhook processed successfully")
            return 'OK', 200
        else:
            logger.warning("Empty update received")
            return 'OK', 200
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return 'Error', 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Railway"""
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'users': len(user_activity),
        'bot_name': bot.get_me().username
    }, 200

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return {
        'message': 'Echo Bot is running!',
        'status': 'active',
        'endpoints': {
            'webhook': '/webhook (POST)',
            'health': '/health (GET)'
        }
    }, 200

# ============ SET WEBHOOK ON STARTUP ============

def set_webhook():
    """Set the webhook URL for the bot"""
    try:
        # Get the Railway URL from environment
        railway_url = os.environ.get('RAILWAY_PUBLIC_DOMAIN')
        if not railway_url:
            logger.warning("RAILWAY_PUBLIC_DOMAIN not set, using polling mode")
            return False
        
        # Remove trailing slash if present
        railway_url = railway_url.rstrip('/')
        webhook_url = f"{railway_url}/webhook"
        
        # Set webhook
        result = bot.set_webhook(url=webhook_url)
        if result:
            logger.info(f"Webhook set successfully to: {webhook_url}")
            return True
        else:
            logger.error("Failed to set webhook")
            return False
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return False

# ============ MAIN ENTRY POINT ============

if __name__ == '__main__':
    logger.info("Starting Echo Bot...")
    
    # Get port from Railway environment
    port = int(os.environ.get('PORT', 5000))
    
    # Set webhook if Railway URL is available
    webhook_set = set_webhook()
    
    if not webhook_set:
        logger.info("Falling back to polling mode...")
        # Start polling in a separate thread
        import threading
        polling_thread = threading.Thread(target=bot.infinity_polling)
        polling_thread.start()
    
    # Start Flask server
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port)
