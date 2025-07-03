# TelegramGiftsChart 🎁

A Telegram bot for generating beautiful gift charts and statistics! 📊

## Features ✨

- Generate visual gift charts and statistics 📈
- Track and manage gift exchanges 🎉
- Beautiful card generation 🖼️
- Database storage for persistent data 💾
- TON integration for payments 💰

## Prerequisites 🛠️

- Python 3.8+
- Telegram Account
- TON Wallet (for payments)

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

3. Set up your Telegram session:
```bash
python src/api/create_session.py
```

4. Configure your bot:
   - Create a bot using [@BotFather](https://t.me/BotFather)
   - Get your API credentials
   - Update the configuration accordingly

## Running the Bot 🤖

To run the bot:
```bash
python bin/bot.py
```

## Testing 🧪

To test the bot functionality, run:
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
│   │   ├── api_client.py
│   │   └── create_session.py
│   ├── config/          # Configuration files
│   │   └── gifts.json   # Gift data configuration
│   ├── database/        # Database operations
│   │   └── database.py
│   ├── generators/      # Image and chart generation
│   │   ├── card_generator.py
│   │   └── chart_generator.py
│   └── utils/          # Utility functions
│       ├── gift_image_utils.py
│       └── utils.py
├── assets/             # Static assets
│   └── ton.png
├── requirements.txt    # Project dependencies
├── setup.py           # Package setup file
└── README.md          # Project documentation
```

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📝

This project is licensed under the MIT License - see the LICENSE file for details.

## Author ✍️

[@Th3ryks](https://t.me/Th3ryks) 
