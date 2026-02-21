# 📈 Sajib Market Trading Monitor Bot

An advanced Telegram bot that provides real-time market monitoring, stock alerts, and financial news with automatic timezone detection.

## ✨ Features

### 🕐 Automatic Timezone Detection
- **Location-based detection**: Send your location to automatically set timezone
- **Manual timezone setting**: Use `/settimezone` command
- **Smart time display**: Shows both market local time and your local time

### 📊 Market Monitoring
- **Multiple markets**: US (NYSE), Malaysia (Bursa), Dhaka (DSE)
- **Real-time status**: Open/closed/lunch break status
- **Weekend detection**: Automatically handles weekend closures
- **Customizable alerts**: Get notified for significant market movements

### 📈 Stock Data
- **Live indices**: Track S&P 500, Dow Jones, NASDAQ, KLSE, DSE
- **Price movements**: Real-time price changes and percentages
- **Smart alerts**: Notifications for 2%+ movements
- **Visual indicators**: 📈📉 emojis for quick status understanding

### 📰 Financial News
- **Latest news**: Real-time financial news from multiple sources
- **Customizable keywords**: Track news relevant to your interests
- **Multiple sources**: Aggregated news from various financial outlets
- **Direct links**: Read full articles with one tap

### ⚙️ User Preferences
- **Personalized settings**: Configure markets, keywords, notifications
- **Toggle notifications**: Enable/disable alerts as needed
- **Market selection**: Choose which markets to monitor
- **News customization**: Set your preferred news keywords

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get API Keys

#### News API (Optional but recommended)
1. Visit [NewsAPI.org](https://newsapi.org/)
2. Sign up for a free account
3. Get your API key
4. Replace `YOUR_NEWS_API_KEY` in the code

### 3. Configure the Bot
1. Your Telegram token is already configured: `8512725996:AAEPtUBWNGxkVk6rZLe2q8emZUsHsYYii-A`
2. If using News API, update the `NEWS_API_KEY` variable

### 4. Run the Bot
```bash
python market_monitor_bot.py
```

## 📱 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot and see main menu |
| `/help` | Show all available commands |
| `/status` | Check current market status |
| `/news` | Get latest financial news |
| `/stocks` | View current stock indices |
| `/settings` | Configure your preferences |
| `/settimezone <tz>` | Set your timezone manually |

### Timezone Examples
- `Asia/Dhaka`
- `Asia/Kuala_Lumpur`
- `America/New_York`
- `Europe/London`
- `Asia/Tokyo`

## 🎯 Usage Tips

### Automatic Timezone Setup
1. **Send your location**: Open Telegram → Attach → Location → Send current location
2. **Bot auto-detects**: Timezone will be automatically set
3. **Manual fallback**: Use `/settimezone` if auto-detection fails

### Getting Market Updates
1. **Quick status**: Use `/status` for current market status
2. **Interactive menu**: Use the inline buttons for easy navigation
3. **Stock alerts**: Enable notifications for automatic alerts

### News Customization
1. **Default keywords**: "stock market", "trading", "finance", "economy"
2. **Custom keywords**: Edit in settings to track specific topics
3. **Real-time updates**: News updates every 30 minutes

## 🔧 Advanced Configuration

### Adding New Markets
Edit the `MARKETS` dictionary in `market_monitor_bot.py`:

```python
"🇨🇦 Canada (TSX)": {
    "tz": "America/Toronto",
    "open": "09:30",
    "close": "16:00",
    "indices": ["^GSPTSE"],
    "currency": "CAD"
}
```

### Custom Stock Symbols
Add your preferred stock symbols to the `indices` list for each market.

### Alert Thresholds
Modify the alert threshold in `send_market_alerts()` method:
```python
if abs(change_percent) > 2.0:  # Change 2.0 to your preferred threshold
```

## 🛠️ Troubleshooting

### Common Issues

#### Bot Not Responding
- Check your internet connection
- Verify the token is correct
- Ensure all dependencies are installed

#### Timezone Detection Not Working
- Install `timezonefinder`: `pip install timezonefinder`
- Try manual timezone setting with `/settimezone`
- Check location permissions in Telegram

#### News Not Working
- Verify your News API key is valid
- Check if you've exceeded API limits
- Ensure `NEWS_API_KEY` is set correctly

#### Stock Data Issues
- Yfinance may have rate limits
- Some symbols might be delisted or unavailable
- Check market hours for real-time data

### Debug Mode
Enable debug logging by modifying the logging level:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Supported Markets

| Market | Exchange | Timezone | Indices Tracked |
|--------|----------|----------|-----------------|
| 🇺🇸 US | NYSE/NASDAQ | America/New_York | S&P 500 (^GSPC), Dow Jones (^DJI), NASDAQ (^IXIC) |
| 🇲🇾 Malaysia | Bursa Malaysia | Asia/Kuala_Lumpur | KLSE (^KLSE) |
| 🇧🇩 Bangladesh | DSE | Asia/Dhaka | DSE Index |

## 🔔 Notification System

The bot sends automatic notifications for:
- **Market movements**: 2%+ changes in tracked indices
- **Market openings**: When markets open (if enabled)
- **Breaking news**: Major financial news (if enabled)

Notifications are sent every 30 minutes during market hours.

## 🌐 API Dependencies

- **Telegram Bot API**: For bot functionality
- **Yahoo Finance**: For stock market data
- **NewsAPI**: For financial news (optional)
- **OpenStreetMap**: For location-based timezone detection
- **TimezoneDB**: For timezone lookup

## 📝 Development Notes

### Code Structure
- **MarketMonitorBot**: Main bot class
- **UserPreferences**: Dataclass for user settings
- **Market functions**: Status checking, stock data, news fetching
- **Scheduler**: Background thread for periodic updates

### Security
- Token is stored securely in the code
- No sensitive data is logged
- User preferences are stored in memory only

## 🤝 Contributing

Feel free to:
- Add new markets
- Improve alert logic
- Add new features
- Fix bugs

## 📄 License

This project is open source. Feel free to modify and distribute.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify your API keys and configuration
3. Ensure all dependencies are installed
4. Contact @Sajib for additional support

---

**Bot Link**: t.me/Sajib_Market_Trading_Monitor_bot
**Token**: 8512725996:AAEPtUBWNGxkVk6rZLe2q8emZUsHsYYii-A
