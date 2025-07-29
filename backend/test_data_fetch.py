import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL")

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

    def submit_order(self, symbol, qty, side, type, time_in_force):
        return self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=type,
            time_in_force=time_in_force
        )

if __name__ == "__main__":
    try:
        service = AlpacaService()
        # Fetch a larger amount of 1-minute data
        bars = service.api.get_bars(
            "SPY",
            "1Min",
            limit=200 # Request more data than long_window (100)
        ).df
        logging.info(f"Fetched {len(bars)} bars for SPY with timeframe 1Min.")
        if len(bars) < 100:
            logging.warning("Still not enough data for SMA Crossover long window.")

    except Exception as e:
        logging.error(f"Error during data fetch test: {e}")