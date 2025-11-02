# Telegram User Simulator - Testing Guide

## Overview

`test_telegram_user.py` is a Python script that simulates Telegram user interactions with your bot. It sends webhook updates in the exact format that Telegram uses, making it perfect for testing without needing to actually use Telegram.

## Prerequisites

1. **Python 3.7+** with `requests` library
2. **Secret Token** - Your bot's `CALLBACK_SECRET` from environment variables
3. **Webhook URL** - Your bot's webhook endpoint (local or deployed)

## Installation

```bash
# Install required dependency
pip install requests
```

## Required Parameters

### 1. Secret Token (REQUIRED)
- **Source**: `CALLBACK_SECRET` environment variable from your bot configuration
- **Purpose**: Authenticates webhook requests (X-Telegram-Bot-Api-Secret-Token header)
- **How to get**: Check your Vercel environment variables or `config_section.py`

### 2. Webhook URL (Optional)
- **Default**: `https://suno-music-bot-test.vercel.app/api/index`
- **Purpose**: Where to send the simulated update
- **Local testing**: `http://localhost:3000/api/index` (if running locally)
- **Production**: Your deployed Vercel URL

## Usage Examples

### Basic Usage

```bash
# Set secret token as environment variable (recommended)
$env:SECRET_TOKEN = "your_secret_token_here"  # PowerShell
export SECRET_TOKEN="your_secret_token_here"   # Bash/Linux

# Send /random command
python test_telegram_user.py --command /random

# Send text message for music generation
python test_telegram_user.py --text "a happy pop song about summer"

# Simulate button click (Repeat button)
python test_telegram_user.py --callback random_repeat
```

### Advanced Usage

```bash
# Custom webhook URL (local development)
python test_telegram_user.py --command /random --webhook-url http://localhost:3000/api/index --secret-token your_token

# Test with different user ID
python test_telegram_user.py --command /random --user-id 999999999

# Test with different language
python test_telegram_user.py --command /random --language ru --username russian_user

# Test callback query
python test_telegram_user.py --callback random_approve --user-id 467981860
```

### Using Environment Variables

```bash
# Set all parameters as environment variables
$env:WEBHOOK_URL = "https://suno-music-bot-test.vercel.app/api/index"
$env:SECRET_TOKEN = "your_secret_token"
$env:USER_ID = "467981860"
$env:LANGUAGE_CODE = "en"

# Then just run commands
python test_telegram_user.py --command /random
python test_telegram_user.py --text "baroque style song about pyramids"
```

## Available Commands

### Commands to Test
- `/start` - User registration
- `/help` - Show help message
- `/about` - Show version info
- `/balance` - Show credit balance
- `/random` - Generate personalized prompt (Phase 3)
- `/history` - Show generation history
- `/transactions` - Show transaction history
- `/upgrade` - Show upgrade options
- `/subscription` - Show subscription status
- `/lyrics` - Export lyrics (Bronze+ tier)

### Callback Queries to Test
- `random_repeat` - Repeat button (generate new prompt)
- `random_approve` - Generate button (approve prompt)
- `buy_sub_bronze` - Buy Bronze subscription
- `buy_sub_silver` - Buy Silver subscription
- `buy_sub_gold` - Buy Gold subscription
- `buy_credits_starter` - Buy Starter credit package
- `buy_credits_value` - Buy Value credit package
- `buy_credits_creator` - Buy Creator credit package

## Testing Scenarios

### 1. Test Phase 3 Personalized Prompts
```bash
# First, generate some music to build profile
python test_telegram_user.py --text "happy pop song about summer"
python test_telegram_user.py --text "energetic rock anthem"

# Then test personalized /random
python test_telegram_user.py --command /random

# Test Repeat button
python test_telegram_user.py --callback random_repeat
```

### 2. Test Interest Extraction
```bash
# Test with pyramids (should extract themes: travel, Egypt, pyramids, sands)
python test_telegram_user.py --text "baroque style song about traveling in Egypt around pyramids"

# Check logs to verify:
# - Moods are inferred (adventurous, mystical, wondrous)
# - Themes include "pyramids"
# - Profile is updated correctly
```

### 3. Test Language Support
```bash
# Russian user
python test_telegram_user.py --command /random --language ru --username russian_user

# Spanish user
python test_telegram_user.py --command /random --language es --username spanish_user
```

### 4. Test New User Flow
```bash
# Use a new user ID (not in database)
python test_telegram_user.py --command /random --user-id 999999999 --username new_user
# Should create user, set default preferences, use default interest profile
```

## Command Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--command` | No* | - | Send a command (e.g., `/random`) |
| `--text` | No* | - | Send a text message |
| `--callback` | No* | - | Simulate button click |
| `--webhook-url` | No | See DEFAULT | Webhook endpoint URL |
| `--secret-token` | Yes** | - | Authentication token |
| `--user-id` | No | 467981860 | Telegram user ID to simulate |
| `--chat-id` | No | Same as user-id | Chat ID |
| `--username` | No | test_user | Username |
| `--language` | No | en | Language code (en, ru, es, etc.) |

\* One of `--command`, `--text`, or `--callback` is required  
\*\* Can be set via `SECRET_TOKEN` environment variable

## Environment Variables

All parameters can be set via environment variables:

```bash
# Windows PowerShell
$env:WEBHOOK_URL = "https://your-bot.vercel.app/api/index"
$env:SECRET_TOKEN = "your_secret_token"
$env:USER_ID = "467981860"
$env:CHAT_ID = "467981860"
$env:USERNAME = "test_user"
$env:LANGUAGE_CODE = "en"
```

```bash
# Linux/Mac Bash
export WEBHOOK_URL="https://your-bot.vercel.app/api/index"
export SECRET_TOKEN="your_secret_token"
export USER_ID="467981860"
export CHAT_ID="467981860"
export USERNAME="test_user"
export LANGUAGE_CODE="en"
```

## Expected Output

```
Sending update to https://suno-music-bot-test.vercel.app/api/index...
Update type: command (/random)
Update data: {
  "update_id": 123456,
  "message": {
    "message_id": 123456,
    "from": {
      "id": 467981860,
      "username": "test_user",
      "language_code": "en"
    },
    "chat": {
      "id": 467981860,
      "type": "private"
    },
    "text": "/random"
  }
}
--------------------------------------------------------------------------------
Response status: 200
Response body: {"ok": true}
--------------------------------------------------------------------------------
✅ Update sent successfully!
```

## Troubleshooting

### Error: "Invalid secret token"
- **Solution**: Check that `SECRET_TOKEN` matches your `CALLBACK_SECRET` configuration
- **Check**: Verify in Vercel environment variables or `config_section.py`

### Error: "Connection refused" or "Timeout"
- **Solution**: Check webhook URL is correct and accessible
- **Local**: Make sure local server is running on correct port
- **Vercel**: Verify deployment URL is correct

### Error: "Update failed with status 500"
- **Solution**: Check bot logs for errors
- **Common causes**: Database connection issues, missing environment variables

### No response from bot
- **Check**: Bot logs should show the update being processed
- **Verify**: Webhook URL is correct and bot is deployed/running
- **Note**: Bot responds asynchronously, may take a few seconds

## Testing Checklist

- [ ] Secret token is set correctly
- [ ] Webhook URL is accessible
- [ ] Commands work (`/random`, `/help`, etc.)
- [ ] Text messages trigger music generation
- [ ] Callback queries work (buttons)
- [ ] User profile builds correctly (Phase 2)
- [ ] Personalized prompts work (Phase 3)
- [ ] Mood inference works (never empty)
- [ ] New interests are preserved (not trimmed immediately)

## Notes

- This script sends updates directly to your webhook, bypassing Telegram
- All updates are simulated - no actual Telegram messages are sent
- User IDs can be any integer - use different IDs to test multiple users
- The script matches Telegram's webhook format exactly
- Responses are logged but bot messages won't appear in Telegram (check logs)

