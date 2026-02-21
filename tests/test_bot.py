import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path to import the bot
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from market_monitor_bot import MarketMonitorBot, UserPreferences, MARKETS

class TestMarketMonitorBot:
    
    @pytest.fixture
    def bot(self):
        """Create a bot instance for testing"""
        with patch('market_monitor_bot.Updater'):
            bot = MarketMonitorBot()
            return bot
    
    @pytest.fixture
    def user_preferences(self):
        """Create user preferences for testing"""
        return UserPreferences(
            chat_id="123456",
            timezone="Asia/Dhaka",
            notifications_enabled=True,
            preferred_markets=["🇺🇸 US (NYSE)", "🇧🇩 Dhaka (DSE)"],
            news_keywords=["stock market", "trading"]
        )
    
    def test_user_preferences_creation(self, user_preferences):
        """Test UserPreferences dataclass"""
        assert user_preferences.chat_id == "123456"
        assert user_preferences.timezone == "Asia/Dhaka"
        assert user_preferences.notifications_enabled is True
        assert len(user_preferences.preferred_markets) == 2
        assert "stock market" in user_preferences.news_keywords
    
    def test_get_market_status_open(self):
        """Test market status when market is open"""
        from datetime import datetime
        import pytz
        
        market_info = MARKETS["🇺🇸 US (NYSE)"]
        bot = MarketMonitorBot()
        
        # Mock current time to be during market hours
        with patch('market_monitor_bot.datetime') as mock_datetime:
            mock_now = Mock()
            mock_now.weekday.return_value = 1  # Tuesday
            mock_now.strftime.return_value = "10:30"
            mock_datetime.datetime.now.return_value = mock_now
            
            with patch('pytz.timezone') as mock_tz:
                mock_tz_obj = Mock()
                mock_tz.return_value = mock_tz_obj
                mock_tz_obj.localize.return_value = mock_now
                
                status = bot.get_market_status("🇺🇸 US (NYSE)", market_info)
                
                assert status["name"] == "🇺🇸 US (NYSE)"
                assert "OPEN" in status["status"]
                assert status["is_open"] is True
    
    def test_get_market_status_closed_weekend(self):
        """Test market status on weekend"""
        from datetime import datetime
        import pytz
        
        market_info = MARKETS["🇺🇸 US (NYSE)"]
        bot = MarketMonitorBot()
        
        # Mock current time to be weekend
        with patch('market_monitor_bot.datetime') as mock_datetime:
            mock_now = Mock()
            mock_now.weekday.return_value = 6  # Sunday
            mock_datetime.datetime.now.return_value = mock_now
            
            with patch('pytz.timezone') as mock_tz:
                mock_tz_obj = Mock()
                mock_tz.return_value = mock_tz_obj
                mock_tz_obj.localize.return_value = mock_now
                
                status = bot.get_market_status("🇺🇸 US (NYSE)", market_info)
                
                assert status["name"] == "🇺🇸 US (NYSE)"
                assert "WEEKEND" in status["status"]
                assert status["is_open"] is False
    
    def test_get_user_timezone_with_preference(self):
        """Test getting user timezone when preference is set"""
        bot = MarketMonitorBot()
        chat_id = "123456"
        
        # Set user preference
        user_preferences[chat_id] = UserPreferences(
            chat_id=chat_id,
            timezone="America/New_York"
        )
        
        timezone = bot.get_user_timezone(chat_id)
        assert timezone == "America/New_York"
    
    def test_get_user_timezone_auto_detect(self):
        """Test automatic timezone detection"""
        bot = MarketMonitorBot()
        chat_id = "789012"
        
        # No user preference set
        with patch('market_monitor_bot.tzlocal.get_localzone') as mock_get_localzone:
            mock_tz = Mock()
            mock_tz.__str__ = lambda x: "Asia/Kuala_Lumpur"
            mock_get_localzone.return_value = mock_tz
            
            timezone = bot.get_user_timezone(chat_id)
            assert timezone == "Asia/Kuala_Lumpur"
    
    @patch('market_monitor_bot.yf.Ticker')
    def test_get_stock_data(self, mock_ticker):
        """Test stock data fetching"""
        bot = MarketMonitorBot()
        symbols = ["^GSPC"]
        
        # Mock yfinance response
        mock_ticker_instance = Mock()
        mock_ticker.return_value = mock_ticker_instance
        mock_ticker_instance.info = {"shortName": "S&P 500"}
        
        mock_history = Mock()
        mock_history.__getitem__ = lambda self, key: [100, 102] if key == 'Close' else [100, 100]
        mock_history.__len__ = lambda self: 2
        mock_history.iloc = Mock()
        mock_history.iloc.__getitem__ = lambda self, key: 102 if key == -1 else 100
        mock_ticker_instance.history.return_value = mock_history
        
        stock_data = bot.get_stock_data(symbols)
        
        assert "^GSPC" in stock_data
        assert stock_data["^GSPC"]["name"] == "S&P 500"
        assert "102.00" in stock_data["^GSPC"]["price"]
    
    def test_detect_timezone_from_location(self):
        """Test timezone detection from coordinates"""
        bot = MarketMonitorBot()
        
        with patch('market_monitor_bot.TimezoneFinder') as mock_tf_class:
            mock_tf = Mock()
            mock_tf_class.return_value = mock_tf
            mock_tf.timezone_at.return_value = "Asia/Dhaka"
            
            timezone = bot.detect_timezone_from_location(23.8103, 90.4125)
            
            assert timezone == "Asia/Dhaka"
            mock_tf.timezone_at.assert_called_once_with(lat=23.8103, lng=90.4125)
    
    def test_market_configuration(self):
        """Test that market configuration is properly set up"""
        assert "🇺🇸 US (NYSE)" in MARKETS
        assert "🇲🇾 Malaysia (Bursa)" in MARKETS
        assert "🇧🇩 Dhaka (DSE)" in MARKETS
        
        us_market = MARKETS["🇺🇸 US (NYSE)"]
        assert us_market["tz"] == "America/New_York"
        assert us_market["open"] == "09:30"
        assert us_market["close"] == "16:00"
        assert "^GSPC" in us_market["indices"]
        
        malaysia_market = MARKETS["🇲🇾 Malaysia (Bursa)"]
        assert "break_start" in malaysia_market
        assert "break_end" in malaysia_market

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
