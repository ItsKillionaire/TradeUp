import logging
import pandas as pd
import numpy
from app.strategies.base import BaseStrategy
from app.services.telegram import TelegramService
from app.core.database import SessionLocal
from app.crud import create_trade
from app.core.connection_manager import manager

class SmaCrossover(BaseStrategy):
    def __init__(self, alpaca_service, short_window=40, long_window=100):
        super().__init__(alpaca_service)
        self.short_window = short_window
        self.long_window = long_window
        self.telegram_service = TelegramService()
        self.db = SessionLocal()

    async def get_position(self, symbol):
        try:
            position = self.alpaca_service.api.get_position(symbol)
            return float(position.qty)
        except Exception as e:
            return 0

    async def run(self, symbol: str, timeframe: str):
        logging.info(f"Running SMA Crossover strategy for {symbol}")
        
        # Fetch historical data
        bars = self.alpaca_service.api.get_bars(
            symbol,
            timeframe,
            limit=self.long_window + 5
        ).df
        logging.info(f"Fetched {len(bars)} bars for {symbol} with timeframe {timeframe}.")

        if len(bars) < self.long_window:
            logging.warning(f"Not enough data for {symbol} to run strategy.")
            return

        # Calculate SMAs
        bars['short_mavg'] = bars['close'].rolling(self.short_window).mean()
        bars['long_mavg'] = bars['close'].rolling(self.long_window).mean()

        # Generate signals
        bars['signal'] = 0
        bars['signal'][self.short_window:] = numpy.where(
            bars['short_mavg'][self.short_window:] > bars['long_mavg'][self.short_window:], 1, 0
        )

        bars['position'] = bars['signal'].diff()

        logging.info(f"Latest signal: {bars['signal'].iloc[-1]}")
        logging.info(f"Latest position change: {bars['position'].iloc[-1]}")

        latest_position = bars['position'].iloc[-1]
        current_position = self.get_position(symbol)
        logging.info(f"Current actual position for {symbol}: {current_position}")

        if latest_position == 1.0 and current_position == 0:
            message = f"Buy signal for {symbol}"
            logging.info(message)
            await self.telegram_service.send_message(message)
            await manager.broadcast(message)
            order = self.alpaca_service.submit_order(symbol, 1, 'buy', 'market', 'gtc')
            create_trade(self.db, symbol, order.qty, order.filled_avg_price, order.side)
            self.google_sheets_service.export_trades()
        elif latest_position == -1.0 and current_position > 0:
            message = f"Sell signal for {symbol}"
            logging.info(message)
            await self.telegram_service.send_message(message)
            await manager.broadcast(message)
            order = self.alpaca_service.submit_order(symbol, current_position, 'sell', 'market', 'gtc')
            create_trade(self.db, symbol, order.qty, order.filled_avg_price, order.side)
            self.google_sheets_service.export_trades()
        else:
            message = f"No signal for {symbol} or already in position"
            logging.info(message)
            await manager.broadcast(message)
