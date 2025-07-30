import alpaca_trade_api as tradeapi
from config import settings
from app.core.connection_manager import manager
from fastapi import HTTPException
import json
import logging

class AlpacaService:
    def __init__(self):
        self.api = tradeapi.REST(
            key_id=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY,
            base_url=settings.ALPACA_BASE_URL,
            api_version='v2'
        )

    async def get_account_info(self):
        try:
            account = self.api.get_account()
            await manager.broadcast_json({"type": "account_update", "data": account._raw})
            return account
        except Exception as e:
            logging.error(f"Error fetching account info: {e}")
            raise HTTPException(status_code=500, detail=f"Error fetching account info: {e}")

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
            raise HTTPException(status_code=500, detail=f"Error submitting order: {e}")
