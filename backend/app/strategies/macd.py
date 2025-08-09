import logging
import pandas as pd
import pandas_ta as ta
from sqlalchemy.orm import Session
from app.strategies.base import BaseStrategy
from app.services.telegram import TelegramService
from app.services.google_sheets import GoogleSheetsService
from app.crud import create_trade
from app.core.connection_manager import manager
from sqlalchemy.orm import Session

class MacdStrategy(BaseStrategy):
    def __init__(self, alpaca_service, telegram_service, google_sheets_service, fast=12, slow=26, signal=9, trade_percentage=0.05, take_profit_pct=0.05, stop_loss_pct=0.02):
        super().__init__(alpaca_service)
        self.fast = fast
        self.slow = slow
        self.signal = signal
        self.trade_percentage = trade_percentage
        self.take_profit_pct = take_profit_pct
        self.stop_loss_pct = stop_loss_pct
        self.telegram_service = telegram_service
        self.google_sheets_service = google_sheets_service

    

    async def run(self, symbol, timeframe, db: Session):
        logging.info(f"Running MACD strategy for {symbol}")
        
        bars = self.alpaca_service.get_bars(
            symbol,
            timeframe,
            limit=self.slow + 5
        ).df
        logging.info(f"Fetched {len(bars)} bars for {symbol} with timeframe {timeframe}.")

        if len(bars) < self.slow:
            logging.warning(f"Not enough data for {symbol} to run strategy.")
            return

        bars.ta.macd(fast=self.fast, slow=self.slow, signal=self.signal, append=True)

        latest_macd = bars[f'MACD_{self.fast}_{self.slow}_{self.signal}'].iloc[-1]
        latest_signal = bars[f'MACDs_{self.fast}_{self.slow}_{self.signal}'].iloc[-1]
        logging.info(f"Latest MACD for {symbol}: {latest_macd:.2f}, Signal: {latest_signal:.2f}")

        current_position = await self.get_position(symbol)

        if latest_macd > latest_signal and current_position == 0:
            message = f"Buy signal for {symbol} (MACD cross)"
            logging.info(message)
            await self.telegram_service.send_message(message)
            await manager.broadcast_json({"type": "log", "message": message})

            account_info = await self.alpaca_service.get_account_info()
            buying_power = float(account_info.buying_power)
            last_price = bars['close'].iloc[-1]
            qty = int((buying_power * self.trade_percentage) / last_price)

            if qty > 0:
                order = self.alpaca_service.submit_order(
                    symbol=symbol, 
                    qty=qty, 
                    side='buy', 
                    type='market', 
                    time_in_force='gtc',
                    order_class='bracket',
                    take_profit={'limit_price': last_price * (1 + self.take_profit_pct)},
                    stop_loss={'stop_price': last_price * (1 - self.stop_loss_pct)}
                )
                create_trade(db, symbol, order.qty, order.filled_avg_price, order.side)
                self.google_sheets_service.export_trades()
        elif latest_macd < latest_signal and current_position > 0:
            message = f"Sell signal for {symbol} (MACD cross)"
            logging.info(message)
            await self.telegram_service.send_message(message)
            await manager.broadcast_json({"type": "log", "message": message})
            order = self.alpaca_service.submit_order(symbol, current_position, 'sell', 'market', 'gtc')
            create_trade(db, symbol, order.qty, order.filled_avg_price, order.side)
            self.google_sheets_service.export_trades()
        else:
            message = f"No signal for {symbol} (MACD cross) or already in position"
            logging.info(message)
            await manager.broadcast_json({"type": "log", "message": message})

    
