import alpaca_trade_api as tradeapi
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL

class AlpacaService:
    def __init__(self):
        self.api = tradeapi.REST(
            key_id=ALPACA_API_KEY,
            secret_key=ALPACA_SECRET_KEY,
            base_url=ALPACA_BASE_URL,
            api_version='v2'
        )

    def get_account_info(self):
        try:
            return self.api.get_account()
        except Exception as e:
            print(f"Error fetching account info: {e}")
            raise

    def submit_order(self, symbol, qty, side, type, time_in_force):
        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=type,
                time_in_force=time_in_force
            )
            logging.info(f"Order submitted: {order}")
            return order
        except Exception as e:
            logging.error(f"Error submitting order: {e}")
            raise
