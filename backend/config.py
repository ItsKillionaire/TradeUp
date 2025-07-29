import os
from dotenv import load_dotenv

load_dotenv()

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(f"ALPACA_API_KEY: {ALPACA_API_KEY}")
print(f"ALPACA_SECRET_KEY: {ALPACA_SECRET_KEY}")
print(f"ALPACA_BASE_URL: {ALPACA_BASE_URL}")
