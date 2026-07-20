# 🤖 Echo Bot for Telegram Ads

A simple, production-ready Echo Bot designed for Telegram Ads approval.

## 🚀 Features
- Echo any text message back
- /start, /help, /about, /ping commands
- Webhook support for Railway
- Health check endpoint
- User activity tracking
- Production-ready logging

## 📦 Deployment on Railway

### Quick Deploy
1. Fork this repository to your GitHub
2. Log in to [Railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your forked repository
5. Add environment variable: `BOT_TOKEN` (get from @BotFather)
6. Deploy!

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| BOT_TOKEN | Your bot token from @BotFather | ✅ Yes |
| RAILWAY_PUBLIC_DOMAIN | Set automatically by Railway | ❌ No |
| PORT | Set automatically by Railway | ❌ No |

## 🔧 Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your BOT_TOKEN
echo "BOT_TOKEN=your_token_here" > .env

# Run the bot
python bot.py
