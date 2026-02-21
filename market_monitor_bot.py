import requests
import datetime
import pytz
import time
import json
import logging
import os
from typing import Dict, List, Optional
from dataclasses import dataclass

# Try to import telegram, handle if not available
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("Warning: python-telegram-bot not available. Bot will run in test mode.")

# Try to import yfinance
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("Warning: yfinance not available. Stock data will be limited.")

# Try to import newsapi
try:
    import newsapi
    NEWSAPI_AVAILABLE = True
except ImportError:
    NEWSAPI_AVAILABLE = False
    print("Warning: newsapi not available. News features will be limited.")

# Try to import geopy
try:
    from geopy.geocoders import Nominatim
    GEOPY_AVAILABLE = True
except ImportError:
    GEOPY_AVAILABLE = False
    print("Warning: geopy not available. Location features will be limited.")

# Try to import tzlocal
try:
    import tzlocal
    TZLOCAL_AVAILABLE = True
except ImportError:
    TZLOCAL_AVAILABLE = False
    print("Warning: tzlocal not available. Timezone detection will be limited.")

import threading
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
    print("Warning: schedule not available. Automated tasks will be limited.")

# --- CONFIGURATION ---
TOKEN = os.environ.get('TELEGRAM_TOKEN', "8512725996:AAEPtUBWNGxkVk6rZLe2q8emZUsHsYYii-A")
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', "YOUR_NEWS_API_KEY")  # Get from https://newsapi.org/

# MARKETS CONFIGURATION
MARKETS = {
    "🇺🇸 US (NYSE)": {
        "tz": "America/New_York", 
        "open": "09:30", 
        "close": "16:00",
        "indices": ["^GSPC", "^DJI", "^IXIC"],  # S&P 500, Dow Jones, NASDAQ
        "currency": "USD"
    },
    "🇲🇾 Malaysia (Bursa)": {
        "tz": "Asia/Kuala_Lumpur", 
        "open": "09:00", 
        "close": "17:00",
        "break_start": "12:30", 
        "break_end": "14:30",
        "indices": ["^KLSE"],
        "currency": "MYR"
    },
    "🇧🇩 Dhaka (DSE)": {
        "tz": "Asia/Dhaka", 
        "open": "10:00", 
        "close": "14:30",
        "indices": ["DSE"],
        "currency": "BDT"
    }
}

# User preferences storage
user_preferences = {}

@dataclass
class UserPreferences:
    chat_id: str
    timezone: Optional[str] = None
    notifications_enabled: bool = True
    preferred_markets: List[str] = None
    news_keywords: List[str] = None
    
    def __post_init__(self):
        if self.preferred_markets is None:
            self.preferred_markets = list(MARKETS.keys())
        if self.news_keywords is None:
            self.news_keywords = ["stock market", "trading", "finance", "economy"]

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MarketMonitorBot:
    def __init__(self):
        if not TELEGRAM_AVAILABLE:
            print("Error: python-telegram-bot is required for this bot to work.")
            return
            
        self.updater = Updater(TOKEN)
        self.dispatcher = self.updater.dispatcher
        
        if NEWSAPI_AVAILABLE and NEWS_API_KEY != "YOUR_NEWS_API_KEY":
            self.news_client = newsapi.NewsApiClient(api_key=NEWS_API_KEY)
        else:
            self.news_client = None
            
        if GEOPY_AVAILABLE:
            self.geolocator = Nominatim(user_agent="market_monitor_bot")
        else:
            self.geolocator = None
            
        self.setup_handlers()
        
    def setup_handlers(self):
        self.dispatcher.add_handler(CommandHandler("start", self.start_command))
        self.dispatcher.add_handler(CommandHandler("help", self.help_command))
        self.dispatcher.add_handler(CommandHandler("status", self.status_command))
        self.dispatcher.add_handler(CommandHandler("news", self.news_command))
        self.dispatcher.add_handler(CommandHandler("stocks", self.stocks_command))
        self.dispatcher.add_handler(CommandHandler("settings", self.settings_command))
        self.dispatcher.add_handler(CommandHandler("settimezone", self.set_timezone_command))
        self.dispatcher.add_handler(CallbackQueryHandler(self.button_callback))
        self.dispatcher.add_handler(MessageHandler(Filters.location, self.handle_location))
        
    def start_command(self, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        
        # Initialize user preferences
        if str(chat_id) not in user_preferences:
            user_preferences[str(chat_id)] = UserPreferences(chat_id=str(chat_id))
        
        welcome_message = """
🚀 *Welcome to Sajib Market Trading Monitor Bot!*

I'll help you stay updated with:
• Real-time market status
• Stock prices and indices
• Latest financial news
• Market crash/increase alerts
• Automatic timezone detection

*Commands:*
/status - Check current market status
/news - Get latest financial news
/stocks - View stock indices
/settings - Configure your preferences
/settimezone - Set your timezone
/help - Show this help message

💡 *Tip:* Send your location for automatic timezone detection!
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 Market Status", callback_data="status")],
            [InlineKeyboardButton("📰 Latest News", callback_data="news")],
            [InlineKeyboardButton("📈 Stock Indices", callback_data="stocks")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="settings")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(welcome_message, parse_mode='Markdown', reply_markup=reply_markup)
        
    def help_command(self, update: Update, context: CallbackContext):
        help_text = """
📖 *Bot Commands Guide*

/start - Start the bot and see main menu
/status - Check current market status for all configured markets
/news - Get latest financial news and market updates
/stocks - View current stock indices and prices
/settings - Configure your notification preferences
/settimezone <timezone> - Set your timezone (e.g., /settimezone Asia/Dhaka)
/help - Show this help message

*Advanced Features:*
📍 Send your location for automatic timezone detection
🔔 Enable/disable notifications for specific markets
📰 Customize news keywords and sources
📊 Track specific stocks and indices

*Timezone Examples:*
• Asia/Dhaka
• Asia/Kuala_Lumpur  
• America/New_York
• Europe/London
• Asia/Tokyo

For more help, contact @Sajib
        """
        update.message.reply_text(help_text, parse_mode='Markdown')
        
    def get_user_timezone(self, chat_id: str) -> str:
        """Get user's timezone, with fallback to auto-detection"""
        user_pref = user_preferences.get(str(chat_id))
        
        if user_pref and user_pref.timezone:
            return user_pref.timezone
            
        # Try to auto-detect timezone
        if TZLOCAL_AVAILABLE:
            try:
                local_tz = tzlocal.get_localzone()
                return str(local_tz)
            except:
                pass  # Fallback to UTC
        
        return "UTC"  # Fallback
            
    def detect_timezone_from_location(self, latitude: float, longitude: float) -> Optional[str]:
        """Detect timezone from coordinates"""
        if not GEOPY_AVAILABLE:
            return None
            
        try:
            from timezonefinder import TimezoneFinder
            tf = TimezoneFinder()
            timezone = tf.timezone_at(lat=latitude, lng=longitude)
            return timezone
        except ImportError:
            logger.warning("timezonefinder not installed, cannot detect timezone from location")
            return None
        except Exception as e:
            logger.error(f"Error detecting timezone: {e}")
            return None
            
    def handle_location(self, update: Update, context: CallbackContext):
        """Handle location messages for automatic timezone detection"""
        chat_id = update.effective_chat.id
        location = update.message.location
        
        timezone = self.detect_timezone_from_location(location.latitude, location.longitude)
        
        if timezone:
            if str(chat_id) not in user_preferences:
                user_preferences[str(chat_id)] = UserPreferences(chat_id=str(chat_id))
            
            user_preferences[str(chat_id)].timezone = timezone
            
            message = f"📍 *Timezone Detected!*\n\nYour timezone has been automatically set to: `{timezone}`\n\nMarket status will now be shown in your local time."
            update.message.reply_text(message, parse_mode='Markdown')
        else:
            update.message.reply_text("❌ Could not detect timezone from your location. Please use /settimezone command.")
            
    def set_timezone_command(self, update: Update, context: CallbackContext):
        """Set user timezone manually"""
        chat_id = update.effective_chat.id
        
        if not context.args:
            update.message.reply_text("Please provide a timezone. Example: /settimezone Asia/Dhaka")
            return
            
        timezone = context.args[0]
        
        # Validate timezone
        try:
            pytz.timezone(timezone)
            
            if str(chat_id) not in user_preferences:
                user_preferences[str(chat_id)] = UserPreferences(chat_id=str(chat_id))
            
            user_preferences[str(chat_id)].timezone = timezone
            
            message = f"✅ *Timezone Updated!*\n\nYour timezone is now set to: `{timezone}`\n\nMarket status will be shown in your local time."
            update.message.reply_text(message, parse_mode='Markdown')
            
        except pytz.exceptions.UnknownTimeZoneError:
            update.message.reply_text("❌ Invalid timezone. Please use a valid timezone like: Asia/Dhaka, America/New_York, etc.")
            
    def get_market_status(self, market_name: str, market_info: dict, user_tz: str = None) -> dict:
        """Get current market status"""
        try:
            market_tz = pytz.timezone(market_info['tz'])
            now = datetime.datetime.now(market_tz)
            current_time = now.strftime("%H:%M")
            
            # Weekend check
            if now.weekday() >= 5:  # Saturday=5, Sunday=6
                status = "🔴 CLOSED (Weekend)"
                is_open = False
            # Lunch break check
            elif "break_start" in market_info and market_info['break_start'] <= current_time <= market_info['break_end']:
                status = "🟡 LUNCH BREAK"
                is_open = False
            # Standard open/close check
            elif market_info['open'] <= current_time <= market_info['close']:
                status = f"🟢 OPEN (Closes at {market_info['close']})"
                is_open = True
            else:
                status = "🔴 CLOSED"
                is_open = False
                
            # Convert to user timezone if provided
            display_time = current_time
            if user_tz and user_tz != market_info['tz']:
                try:
                    user_tz_obj = pytz.timezone(user_tz)
                    user_time = now.astimezone(user_tz_obj)
                    display_time = f"{current_time} ({user_time.strftime('%H:%M')} your time)"
                except:
                    pass
                    
            return {
                "name": market_name,
                "local_time": current_time,
                "display_time": display_time,
                "status": status,
                "is_open": is_open,
                "currency": market_info.get('currency', 'USD')
            }
            
        except Exception as e:
            logger.error(f"Error getting market status for {market_name}: {e}")
            return {
                "name": market_name,
                "local_time": "N/A",
                "display_time": "N/A",
                "status": "❌ ERROR",
                "is_open": False,
                "currency": "USD"
            }
            
    def get_stock_data(self, symbols: List[str]) -> Dict[str, dict]:
        """Get current stock data for given symbols"""
        stock_data = {}
        
        if not YFINANCE_AVAILABLE:
            # Return mock data if yfinance is not available
            for symbol in symbols:
                stock_data[symbol] = {
                    "symbol": symbol,
                    "name": symbol,
                    "price": "N/A",
                    "change": "N/A",
                    "change_percent": "N/A"
                }
            return stock_data
        
        for symbol in symbols:
            try:
                if symbol == "DSE":  # Special handling for DSE
                    stock_data[symbol] = {
                        "symbol": symbol,
                        "name": "DSE Index",
                        "price": "N/A",
                        "change": "N/A",
                        "change_percent": "N/A"
                    }
                    continue
                    
                ticker = yf.Ticker(symbol)
                info = ticker.info
                history = ticker.history(period="1d")
                
                if not history.empty:
                    current_price = history['Close'].iloc[-1]
                    previous_close = history['Open'].iloc[0]
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100
                    
                    stock_data[symbol] = {
                        "symbol": symbol,
                        "name": info.get('shortName', symbol),
                        "price": f"{current_price:.2f}",
                        "change": f"{change:+.2f}",
                        "change_percent": f"{change_percent:+.2f}%"
                    }
                    
            except Exception as e:
                logger.error(f"Error fetching data for {symbol}: {e}")
                stock_data[symbol] = {
                    "symbol": symbol,
                    "name": symbol,
                    "price": "N/A",
                    "change": "N/A",
                    "change_percent": "N/A"
                }
                
        return stock_data
        
    def get_market_news(self, keywords: List[str] = None) -> List[dict]:
        """Get latest market news"""
        if not self.news_client:
            return []
            
        try:
            if not keywords:
                keywords = ["stock market", "trading", "finance", "economy"]
                
            query = " OR ".join(keywords)
            news = self.news_client.get_everything(
                q=query,
                language='en',
                sort_by='publishedAt',
                page_size=10
            )
            
            articles = []
            for article in news.get('articles', [])[:5]:  # Limit to 5 articles
                articles.append({
                    "title": article.get('title', ''),
                    "description": article.get('description', ''),
                    "url": article.get('url', ''),
                    "source": article.get('source', {}).get('name', ''),
                    "published_at": article.get('publishedAt', '')
                })
                
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []
            
    def status_command(self, update: Update, context: CallbackContext):
        """Show current market status"""
        chat_id = update.effective_chat.id
        user_tz = self.get_user_timezone(chat_id)
        
        message = "🔔 *Market Status Update*\n\n"
        
        for market_name, market_info in MARKETS.items():
            status = self.get_market_status(market_name, market_info, user_tz)
            message += f"*{status['name']}*\n"
            message += f"Local Time: {status['display_time']}\n"
            message += f"Status: {status['status']}\n\n"
            
        update.message.reply_text(message, parse_mode='Markdown')
        
    def news_command(self, update: Update, context: CallbackContext):
        """Show latest market news"""
        chat_id = update.effective_chat.id
        user_pref = user_preferences.get(str(chat_id))
        
        keywords = user_pref.news_keywords if user_pref else None
        articles = self.get_market_news(keywords)
        
        if not articles:
            update.message.reply_text("❌ Could not fetch news. Please check your News API configuration.")
            return
            
        message = "📰 *Latest Market News*\n\n"
        
        for i, article in enumerate(articles, 1):
            message += f"*{i}. {article['title']}*\n"
            message += f"{article['description']}\n"
            message += f"📰 {article['source']}\n"
            message += f"[Read more]({article['url']})\n\n"
            
        update.message.reply_text(message, parse_mode='Markdown', disable_web_page_preview=True)
        
    def stocks_command(self, update: Update, context: CallbackContext):
        """Show stock indices"""
        message = "📈 *Stock Indices*\n\n"
        
        all_symbols = []
        for market_info in MARKETS.values():
            all_symbols.extend(market_info.get('indices', []))
            
        stock_data = self.get_stock_data(all_symbols)
        
        for symbol, data in stock_data.items():
            emoji = "📈" if data['change_percent'].startswith('+') else "📉" if data['change_percent'].startswith('-') else "➡️"
            message += f"{emoji} *{data['name']} ({symbol})*\n"
            message += f"Price: {data['price']}\n"
            message += f"Change: {data['change']} ({data['change_percent']})\n\n"
            
        update.message.reply_text(message, parse_mode='Markdown')
        
    def settings_command(self, update: Update, context: CallbackContext):
        """Show settings menu"""
        chat_id = update.effective_chat.id
        user_pref = user_preferences.get(str(chat_id))
        
        if not user_pref:
            user_pref = UserPreferences(chat_id=str(chat_id))
            user_preferences[str(chat_id)] = user_pref
            
        message = "⚙️ *Your Settings*\n\n"
        message += f"🕐 Timezone: `{user_pref.timezone or 'Auto-detect'}`\n"
        message += f"🔔 Notifications: {'✅ Enabled' if user_pref.notifications_enabled else '❌ Disabled'}\n"
        message += f"📊 Tracked Markets: {len(user_pref.preferred_markets)}\n"
        message += f"📰 News Keywords: {', '.join(user_pref.news_keywords[:3])}...\n\n"
        
        keyboard = [
            [InlineKeyboardButton("🕐 Set Timezone", callback_data="set_timezone")],
            [InlineKeyboardButton("🔔 Toggle Notifications", callback_data="toggle_notifications")],
            [InlineKeyboardButton("📊 Select Markets", callback_data="select_markets")],
            [InlineKeyboardButton("📰 Edit Keywords", callback_data="edit_keywords")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)
        
    def button_callback(self, update: Update, context: CallbackContext):
        """Handle button callbacks"""
        query = update.callback_query
        query.answer()
        
        data = query.data
        
        if data == "status":
            self.status_command(update, context)
        elif data == "news":
            self.news_command(update, context)
        elif data == "stocks":
            self.stocks_command(update, context)
        elif data == "settings":
            self.settings_command(update, context)
        elif data == "set_timezone":
            query.edit_message_text(
                "🕐 *Set Your Timezone*\n\n"
                "Please send your location for automatic detection, "
                "or use /settimezone <timezone> command.\n\n"
                "Examples: Asia/Dhaka, America/New_York, Europe/London",
                parse_mode='Markdown'
            )
        elif data == "toggle_notifications":
            chat_id = update.effective_chat.id
            user_pref = user_preferences.get(str(chat_id))
            if user_pref:
                user_pref.notifications_enabled = not user_pref.notifications_enabled
                status = "enabled" if user_pref.notifications_enabled else "disabled"
                query.edit_message_text(f"✅ Notifications {status}!")
        elif data == "select_markets":
            # Create market selection keyboard
            keyboard = []
            for market_name in MARKETS.keys():
                keyboard.append([InlineKeyboardButton(market_name, callback_data=f"market_{market_name}")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text("📊 *Select Markets to Track*\n\nChoose which markets you want to monitor:", 
                                  parse_mode='Markdown', reply_markup=reply_markup)
                                  
    def send_market_alerts(self):
        """Send periodic market alerts"""
        for chat_id_str, user_pref in user_preferences.items():
            if not user_pref.notifications_enabled:
                continue
                
            try:
                # Check for significant market movements
                alerts = []
                
                for market_name in user_pref.preferred_markets:
                    if market_name in MARKETS:
                        market_info = MARKETS[market_name]
                        symbols = market_info.get('indices', [])
                        
                        if symbols:
                            stock_data = self.get_stock_data(symbols)
                            
                            for symbol, data in stock_data.items():
                                try:
                                    change_percent = float(data['change_percent'].replace('%', '').replace('+', ''))
                                    if abs(change_percent) > 2.0:  # Alert on 2%+ movement
                                        direction = "🚀" if change_percent > 0 else "📉"
                                        alerts.append(f"{direction} {data['name']}: {data['change_percent']}")
                                except:
                                    continue
                                    
                if alerts:
                    message = f"🚨 *Market Alert*\n\n" + "\n".join(alerts[:5])  # Limit to 5 alerts
                    
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                    payload = {
                        "chat_id": chat_id_str,
                        "text": message,
                        "parse_mode": "Markdown"
                    }
                    requests.post(url, json=payload)
                    
            except Exception as e:
                logger.error(f"Error sending alerts to {chat_id_str}: {e}")
                
    def run(self):
        """Start the bot"""
        if not TELEGRAM_AVAILABLE:
            print("Cannot start bot: python-telegram-bot is not available.")
            return
            
        logger.info("Starting Market Monitor Bot...")
        
        # Schedule periodic alerts
        if SCHEDULE_AVAILABLE:
            schedule.every(30).minutes.do(self.send_market_alerts)
            
            def run_scheduler():
                while True:
                    schedule.run_pending()
                    time.sleep(60)
                
            scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            scheduler_thread.start()
        
        self.updater.start_polling()
        self.updater.idle()

if __name__ == "__main__":
    bot = MarketMonitorBot()
    bot.run()
