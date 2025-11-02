"""
Telegram User Simulator Script

This script simulates a Telegram user interacting with the bot for testing purposes.
It sends webhook updates in the same format that Telegram sends.

Usage:
    python test_telegram_user.py --command /random
    python test_telegram_user.py --text "a happy pop song about summer"
    python test_telegram_user.py --callback random_repeat

Parameters (via environment variables or command line):
    - WEBHOOK_URL: Full URL to webhook endpoint (default: http://localhost:3000/api/index)
    - SECRET_TOKEN: X-Telegram-Bot-Api-Secret-Token (required, from CALLBACK_SECRET)
    - USER_ID: Telegram user ID to simulate (default: 123456789)
    - CHAT_ID: Chat ID (default: same as USER_ID)
    - USERNAME: Username (default: "test_user")
    - LANGUAGE_CODE: User language (default: "en")
"""

import argparse
import json
import os
import sys
import requests
from datetime import datetime
from typing import Optional, Dict, Any

# Default configuration
DEFAULT_WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:3000/api/index")
DEFAULT_SECRET_TOKEN = os.getenv("SECRET_TOKEN", "")
DEFAULT_USER_ID = int(os.getenv("USER_ID", "123456789"))
DEFAULT_CHAT_ID = int(os.getenv("CHAT_ID", str(DEFAULT_USER_ID)))
DEFAULT_USERNAME = os.getenv("USERNAME", "test_user")
DEFAULT_LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en")


def create_message_update(
    text: str,
    user_id: int = DEFAULT_USER_ID,
    chat_id: int = DEFAULT_CHAT_ID,
    username: str = DEFAULT_USERNAME,
    language_code: str = DEFAULT_LANGUAGE_CODE,
    message_id: int = None
) -> Dict[str, Any]:
    """
    Create a Telegram Update object for a text message.
    
    Args:
        text: Message text content
        user_id: Telegram user ID
        chat_id: Chat ID
        username: Username
        language_code: User language code
        message_id: Optional message ID (auto-generated if None)
    
    Returns:
        Update object as dictionary
    """
    if message_id is None:
        message_id = int(datetime.now().timestamp() * 1000) % 1000000
    
    update = {
        "update_id": message_id,
        "message": {
            "message_id": message_id,
            "from": {
                "id": user_id,
                "is_bot": False,
                "first_name": username.capitalize(),
                "username": username,
                "language_code": language_code
            },
            "chat": {
                "id": chat_id,
                "type": "private",
                "username": username,
                "first_name": username.capitalize()
            },
            "date": int(datetime.now().timestamp()),
            "text": text
        }
    }
    
    return update


def create_command_update(
    command: str,
    user_id: int = DEFAULT_USER_ID,
    chat_id: int = DEFAULT_CHAT_ID,
    username: str = DEFAULT_USERNAME,
    language_code: str = DEFAULT_LANGUAGE_CODE,
    message_id: int = None
) -> Dict[str, Any]:
    """
    Create a Telegram Update object for a command.
    
    Args:
        command: Command text (e.g., "/random", "/help")
        user_id: Telegram user ID
        chat_id: Chat ID
        username: Username
        language_code: User language code
        message_id: Optional message ID
    
    Returns:
        Update object as dictionary
    """
    # Create base message update
    update = create_message_update(command, user_id, chat_id, username, language_code, message_id)
    
    # Add BOT_COMMAND entity so PTB recognizes it as a command
    # Telegram's MessageEntity.BOT_COMMAND type is 2
    command_length = len(command.split()[0])  # Length of command without arguments
    update["message"]["entities"] = [
        {
            "type": "bot_command",
            "offset": 0,
            "length": command_length
        }
    ]
    
    return update


def create_callback_query_update(
    callback_data: str,
    user_id: int = DEFAULT_USER_ID,
    chat_id: int = DEFAULT_CHAT_ID,
    username: str = DEFAULT_USERNAME,
    message_id: int = None
) -> Dict[str, Any]:
    """
    Create a Telegram Update object for a callback query (button click).
    
    Args:
        callback_data: Callback data (e.g., "random_repeat", "random_approve")
        user_id: Telegram user ID
        chat_id: Chat ID
        username: Username
        message_id: Optional message ID for the message with the button
    
    Returns:
        Update object as dictionary
    """
    if message_id is None:
        message_id = int(datetime.now().timestamp() * 1000) % 1000000
    
    update_id = int(datetime.now().timestamp() * 1000) % 1000000
    
    update = {
        "update_id": update_id,
        "callback_query": {
            "id": f"test_callback_{update_id}",
            "from": {
                "id": user_id,
                "is_bot": False,
                "first_name": username.capitalize(),
                "username": username
            },
            "message": {
                "message_id": message_id,
                "from": {
                    "id": DEFAULT_USER_ID,  # Bot's user ID (not needed but included for completeness)
                    "is_bot": True,
                    "first_name": "Suno Music Bot",
                    "username": "sunomusicbot"
                },
                "chat": {
                    "id": chat_id,
                    "type": "private",
                    "username": username,
                    "first_name": username.capitalize()
                },
                "date": int(datetime.now().timestamp()),
                "text": "Random prompt test message"
            },
            "chat_instance": f"test_instance_{user_id}",
            "data": callback_data
        }
    }
    
    return update


def send_update(
    update: Dict[str, Any],
    webhook_url: str = DEFAULT_WEBHOOK_URL,
    secret_token: str = DEFAULT_SECRET_TOKEN
) -> requests.Response:
    """
    Send a Telegram Update to the webhook.
    
    Args:
        update: Update object as dictionary
        webhook_url: Webhook URL endpoint
        secret_token: Secret token for authentication
    
    Returns:
        HTTP response object
    """
    headers = {
        "Content-Type": "application/json",
        "X-Telegram-Bot-Api-Secret-Token": secret_token
    }
    
    # Extract user info for warning
    user_id = None
    if "message" in update:
        user_id = update["message"].get("from", {}).get("id")
    elif "callback_query" in update:
        user_id = update["callback_query"].get("from", {}).get("id")
    
    print("=" * 80)
    print("WARNING: This script sends REAL webhook requests to your bot!")
    print(f"WARNING: Messages will appear in Telegram for user ID: {user_id}")
    print("WARNING: To avoid affecting your real account, use --user-id with a test ID")
    print("=" * 80)
    print(f"Sending update to {webhook_url}...")
    print(f"Update type: {get_update_type(update)}")
    print(f"Update data: {json.dumps(update, indent=2)}")
    print("-" * 80)
    
    try:
        response = requests.post(
            webhook_url,
            json=update,
            headers=headers,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        print("-" * 80)
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"Error sending update: {e}")
        raise


def get_update_type(update: Dict[str, Any]) -> str:
    """Get the type of update (message, callback_query, etc.)"""
    if "message" in update:
        text = update["message"].get("text", "")
        if text and text.startswith("/"):
            return f"command ({text})"
        return "message"
    elif "callback_query" in update:
        return f"callback_query ({update['callback_query'].get('data', '')})"
    else:
        return "unknown"


def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(
        description="Simulate a Telegram user interacting with the bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send /random command
  python test_telegram_user.py --command /random

  # Send text message
  python test_telegram_user.py --text "a happy pop song about summer"

  # Click Repeat button
  python test_telegram_user.py --callback random_repeat

  # With custom user ID and language
  python test_telegram_user.py --command /random --user-id 123456 --language ru

Environment Variables:
  WEBHOOK_URL - Webhook endpoint URL (default: http://localhost:3000/api/index)
  SECRET_TOKEN - Secret token for authentication (required)
  USER_ID - Telegram user ID (default: 123456789)
  CHAT_ID - Chat ID (default: same as USER_ID)
  USERNAME - Username (default: test_user)
  LANGUAGE_CODE - User language (default: en)
        """
    )
    
    parser.add_argument(
        "--command",
        type=str,
        help="Send a command (e.g., /random, /help, /balance)"
    )
    
    parser.add_argument(
        "--text",
        type=str,
        help="Send a text message (for music generation)"
    )
    
    parser.add_argument(
        "--callback",
        type=str,
        help="Simulate callback query (button click), e.g., random_repeat, random_approve"
    )
    
    parser.add_argument(
        "--webhook-url",
        type=str,
        default=DEFAULT_WEBHOOK_URL,
        help=f"Webhook URL (default: {DEFAULT_WEBHOOK_URL})"
    )
    
    parser.add_argument(
        "--secret-token",
        type=str,
        default=DEFAULT_SECRET_TOKEN,
        help="Secret token for authentication (required)"
    )
    
    parser.add_argument(
        "--user-id",
        type=int,
        default=DEFAULT_USER_ID,
        help=f"Telegram user ID (default: {DEFAULT_USER_ID})"
    )
    
    parser.add_argument(
        "--chat-id",
        type=int,
        default=None,
        help="Chat ID (default: same as user-id)"
    )
    
    parser.add_argument(
        "--username",
        type=str,
        default=DEFAULT_USERNAME,
        help=f"Username (default: {DEFAULT_USERNAME})"
    )
    
    parser.add_argument(
        "--language",
        type=str,
        default=DEFAULT_LANGUAGE_CODE,
        help=f"Language code (default: {DEFAULT_LANGUAGE_CODE})"
    )
    
    args = parser.parse_args()
    
    # Validate secret token
    secret_token = args.secret_token or os.getenv("SECRET_TOKEN", "")
    if not secret_token:
        print("ERROR: Secret token is required!")
        print("Set SECRET_TOKEN environment variable or use --secret-token argument")
        print("Get the token from your bot's CALLBACK_SECRET configuration")
        sys.exit(1)
    
    chat_id = args.chat_id if args.chat_id is not None else args.user_id
    
    # Determine which action to perform
    if args.command:
        update = create_command_update(
            args.command,
            args.user_id,
            chat_id,
            args.username,
            args.language
        )
    elif args.text:
        update = create_message_update(
            args.text,
            args.user_id,
            chat_id,
            args.username,
            args.language
        )
    elif args.callback:
        update = create_callback_query_update(
            args.callback,
            args.user_id,
            chat_id,
            args.username
        )
    else:
        print("ERROR: Must specify --command, --text, or --callback")
        parser.print_help()
        sys.exit(1)
    
    # Send the update
    try:
        response = send_update(
            update,
            args.webhook_url,
            secret_token
        )
        
        if response.status_code == 200:
            print("[SUCCESS] Update sent successfully!")
        else:
            print(f"[ERROR] Update failed with status {response.status_code}")
            if response.text:
                print(f"Response: {response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

