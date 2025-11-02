# Telegram Bot Tester

Standalone Python script to test Telegram bot webhooks by simulating user interactions.

## Installation

```bash
pip install -r requirements_test.txt
```

## Usage

```bash
# Set your secret token
export SECRET_TOKEN="your_secret_token_here"

# Send commands
python test_telegram_user.py --command /start --user-id 123456

# Send text messages
python test_telegram_user.py --text "a happy song"

# Simulate button clicks
python test_telegram_user.py --callback random_repeat
```

## Requirements

- Python 3.7+
- requests library

## Configuration

- `SECRET_TOKEN`: Your bot's CALLBACK_SECRET (required)
- `WEBHOOK_URL`: Bot webhook endpoint (default: from env or test URL)
- `USER_ID`: Telegram user ID to simulate (default: 467981860)

See `TEST_USER_GUIDE.md` for detailed documentation.