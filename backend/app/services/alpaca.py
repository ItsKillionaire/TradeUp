import alpaca_trade_api as tradeapi
from config import settings
from app.core.connection_manager import manager
from fastapi import HTTPException
import json
import logging

class AlpacaService:
    def __init__(self):
        # Client for trading and account management
        self.api = tradeapi.REST(
            key_id=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY,
            base_url=settings.ALPACA_BASE_URL, # Should point to paper or live
            api_version='v2'
        )

        # Client specifically for fetching market data
        self.data_api = tradeapi.REST(
            key_id=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY,
            base_url="https://paper-api.alpaca.markets", # Always use paper for data in this context
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

    def get_bars(self, symbol, timeframe, limit):
        try:
            bars = self.data_api.get_bars(
                symbol,
                timeframe,
                limit=limit
            )
            return bars
        except Exception as e:
            logging.error(f"Error fetching bars: {e}")
            raise HTTPException(status_code=500, detail=f"Error fetching bars: {e}")

    def submit_order(self, symbol, side, type, time_in_force, qty=None, notional=None, order_class=None, take_profit=None, stop_loss=None):
        try:
            if not qty and not notional:
                raise ValueError("Either 'qty' or 'notional' must be provided.")
            if qty and notional:
                raise ValueError("Provide 'qty' or 'notional', not both.")

            order_data = {
                'symbol': symbol,
                'side': side,
                'type': type,
                'time_in_force': time_in_force,
            }
            if qty:
                order_data['qty'] = qty
            if notional:
                order_data['notional'] = notional
            if order_class:
                order_data['order_class'] = order_class
            if take_profit:
                order_data['take_profit'] = take_profit
            if stop_loss:
                order_data['stop_loss'] = stop_loss

            order = self.api.submit_order(**order_data)
            logging.info(f"Order submitted: {order}")
            return order
        except Exception as e:
            logging.error(f"Error submitting order: {e}")
            raise HTTPException(status_code=500, detail=f"Error submitting order: {e}")

    def get_open_positions(self):
        try:
            positions = self.api.list_positions()
            orders = self.api.list_orders(status='open')
            positions_data = []
            for p in positions:
                position_dict = p._raw
                related_orders = [o for o in orders if o.symbol == p.symbol]
                if related_orders:
                    for o in related_orders:
                        if hasattr(o, 'take_profit') and o.take_profit:
                            position_dict['take_profit_price'] = o.take_profit['limit_price']
                        if hasattr(o, 'stop_loss') and o.stop_loss:
                            position_dict['stop_loss_price'] = o.stop_loss['stop_price']
                positions_data.append(position_dict)
            return positions_data
        except Exception as e:
            logging.error(f"Error fetching open positions: {e}")
            raise HTTPException(status_code=500, detail=f"Error fetching open positions: {e}")

    def get_orders(self):
        try:
            orders = self.api.list_orders(status='all', limit=100) # Fetches last 100 orders
            return [o._raw for o in orders]
        except Exception as e:
            logging.error(f"Error fetching orders: {e}")
            raise HTTPException(status_code=500, detail=f"Error fetching orders: {e}")

    def get_clock(self):
        try:
            return self.api.get_clock()
        except Exception as e:
            logging.error(f"Error fetching clock: {e}")
            raise HTTPException(status_code=500, detail=f"Error fetching clock: {e}")
