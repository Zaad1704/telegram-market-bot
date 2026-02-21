import os
import sys

# Fix for Replit environment
os.environ['PYTHONUNBUFFERED'] = '1'

# Import the main bot
from market_monitor_bot import *

if __name__ == "__main__":
    # Override config with environment variables
    TOKEN = os.environ.get('TELEGRAM_TOKEN', "8512725996:AAEPtUBWNGxkVk6rZLe2q8emZUsHsYYii-A")
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY', "YOUR_NEWS_API_KEY")
    
    # Create and run bot
    bot = MarketMonitorBot()
    bot.run()
