# TelegramGiftsChart 🎁

A Telegram bot for generating beautiful gift charts and statistics! 📊

## Features ✨

- Generate visual gift charts and statistics 📈
- Track gift prices in real-time 📊
- Beautiful card generation with price history 🖼️
- Rate limiting for user requests ⏱️
- Smart gift name suggestions 🎯
- TON integration for price tracking 💰

## Prerequisites 🛠️

- Python 3.8+
- Telegram Account
- Telegram API credentials (API ID and Hash)
- Bot Token from [@BotFather](https://t.me/BotFather)

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/Th3ryks/TelegramGiftsChart.git
cd TelegramGiftsChart
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your credentials:
```env
# Telegram Bot Token (from @BotFather)
TELEGRAM_BOT_TOKEN='your_bot_token_here'

# Telegram API Credentials (from https://my.telegram.org/apps)
API_ID='your_api_id_here'
API_HASH='your_api_hash_here'
PHONE_NUMBER='your_phone_number_here'
```

4. Set up your Telegram session:
```bash
python src/api/create_session.py
```
Follow the prompts to enter your phone number and the verification code.

## Configuration ⚙️

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from @BotFather | Yes |
| `API_ID` | Telegram API ID from my.telegram.org | Yes |
| `API_HASH` | Telegram API hash from my.telegram.org | Yes |
| `PHONE_NUMBER` | Your phone number | Yes |

### Rate Limiting

The bot includes rate limiting to prevent spam:
- 10 seconds cooldown between requests per user
- Configurable in `bin/bot.py` via `RATE_LIMIT_SECONDS`

## Running the Bot 🤖

To run the bot:
```bash
python bin/bot.py
```

The bot will start and show connection status in the console.

### Bot Commands

- `/start` - Start the bot and get welcome message
- Send any gift name to get its price chart (e.g., "Crystal Ball", "Plush Pepe")

## Testing 🧪

To test the bot functionality:
```bash
python bin/test.py
```

## Project Structure 📁

```
TelegramGiftsChart/
├── bin/                  # Executable files
│   ├── bot.py           # Main bot executable
│   └── test.py          # Test script
├── src/
│   ├── api/             # API related files
│   │   ├── api_client.py        # API interaction logic
│   │   └── create_session.py    # Session creation script
│   ├── config/          # Configuration files
│   │   └── gifts.json   # Gift data configuration
│   ├── database/        # Database operations
│   │   └── database.py  # SQLite database handling
│   ├── generators/      # Image and chart generation
│   │   ├── card_generator.py    # Gift card image generation
│   │   └── chart_generator.py   # Price chart generation
│   └── utils/           # Utility functions
│       ├── gift_image_utils.py  # Image processing utilities
│       └── utils.py             # General utilities
├── assets/             # Static assets
│   └── ton.png        # TON currency logo
├── requirements.txt    # Project dependencies
├── setup.py           # Package setup file
└── README.md          # Project documentation
```

## Error Handling 🔧

The bot includes comprehensive error handling:
- Graceful handling of blocked users
- Rate limiting protection
- Network error recovery
- User-friendly error messages

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📝

This project is licensed under the MIT License - see the LICENSE file for details.

## Author ✍️

[@Th3ryks](https://github.com/Th3ryks) 
