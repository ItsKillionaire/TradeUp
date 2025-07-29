import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

load_dotenv()

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL")

print(f"ALPACA_API_KEY: {ALPACA_API_KEY}")
print(f"ALPACA_SECRET_KEY: {ALPACA_SECRET_KEY}")
print(f"ALPACA_BASE_URL: {ALPACA_BASE_URL}")

class AlpacaService:
    def __init__(self):
        self.api = tradeapi.REST(
            key_id=ALPACA_API_KEY,
            secret_key=ALPACA_SECRET_KEY,
            base_url=ALPACA_BASE_URL,
            api_version='v2'
        )

    def get_account_info(self):
        return self.api.get_account()

if __name__ == "__main__":
    try:
        service = AlpacaService()
        account_info = service.get_account_info()
        print("Account Info:", account_info)
    except Exception as e:
        print(f"Error during AlpacaService test: {e}")