# Configuration file for Sajib Market Trading Monitor Bot
# Copy this file and rename to config_local.py for your local settings

# --- TELEGRAM BOT CONFIGURATION ---
TOKEN = "8512725996:AAEPtUBWNGxkVk6rZLe2q8emZUsHsYYii-A"

# --- API KEYS ---
# Get your free API key from: https://newsapi.org/
NEWS_API_KEY = "YOUR_NEWS_API_KEY"

# --- ALERT SETTINGS ---
ALERT_THRESHOLD_PERCENT = 2.0  # Send alerts for movements > 2%
ALERT_INTERVAL_MINUTES = 30    # Check for alerts every 30 minutes

# --- RATE LIMITING ---
MAX_REQUESTS_PER_MINUTE = 30   # Respect API rate limits
REQUEST_TIMEOUT_SECONDS = 10   # Timeout for API requests

# --- LOGGING ---
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "bot.log"  # Set to None for console only

# --- MARKET CONFIGURATION ---
# You can override or extend the markets here
ADDITIONAL_MARKETS = {
    # "🇸🇬 Singapore (SGX)": {
    #     "tz": "Asia/Singapore",
    #     "open": "09:00",
    #     "close": "17:00",
    #     "indices": ["^STI"],
    #     "currency": "SGD"
    # }
}

# --- USER PREFERENCES DEFAULTS ---
DEFAULT_NOTIFICATIONS_ENABLED = True
DEFAULT_TIMEZONE = None  # Auto-detect
DEFAULT_NEWS_KEYWORDS = ["stock market", "trading", "finance", "economy"]

# --- DEVELOPMENT SETTINGS ---
DEBUG_MODE = False  # Enable for detailed logging
TEST_MODE = False   # Enable for testing without real API calls
