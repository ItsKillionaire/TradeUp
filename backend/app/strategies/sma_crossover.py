import logging
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.strategies.base import BaseStrategy
from app.services.telegram import TelegramService
from app.services.google_sheets import GoogleSheetsService
from app.crud import create_trade
from app.core.connection_manager import manager
from sqlalchemy.orm import Session

class SmaCrossover(BaseStrategy):
    def __init__(self, alpaca_service, telegram_service, google_sheets_service, short_window=40, long_window=100, trade_percentage=0.05, take_profit_pct=0.05, stop_loss_pct=0.02):
        super().__init__(alpaca_service, "SMA Crossover")
        self.short_window = short_window
        self.long_window = long_window
        self.trade_percentage = trade_percentage
        self.take_profit_pct = take_profit_pct
        self.stop_loss_pct = stop_loss_pct
        self.telegram_service = telegram_service
        self.google_sheets_service = google_sheets_service

    

    async def run(self, symbol, timeframe, db: Session):
        logging.info(f"Running SMA Crossover strategy for {symbol}")
        
        # Fetch historical data
        bars = self.alpaca_service.get_bars(
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
        bars.loc[bars.index[self.short_window:], 'signal'] = np.where(
            bars['short_mavg'][self.short_window:] > bars['long_mavg'][self.short_window:], 1, 0
        )

        bars['position'] = bars['signal'].diff()

        latest_position = bars['position'].iloc[-1]
        current_position_qty = await self.get_position(symbol)
        logging.info(f"Current position for {symbol}: {current_position_qty} shares.")

        short_mavg = bars['short_mavg'].iloc[-1]
        long_mavg = bars['long_mavg'].iloc[-1]

        if latest_position == 1.0 and current_position_qty == 0:
            account_info = await self.alpaca_service.get_account_info()
            buying_power = float(account_info.buying_power)
            notional_to_trade = buying_power * self.trade_percentage
            last_price = bars['close'].iloc[-1]

            message = (
                f"TRADE SIGNAL: Buy {symbol}.\n"
                f"Reason: SMA Crossover (Short {self.short_window} SMA crossed above Long {self.long_window} SMA).\n"
                f"  - Short SMA: {short_mavg:.2f}\n"
                f"  - Long SMA: {long_mavg:.2f}\n"
                f"  - Current Price: {last_price:.2f}\n"
                f"  - Account Buying Power: ${buying_power:,.2f}\n"
                f"  - Position Size (Notional): ${notional_to_trade:,.2f} ({self.trade_percentage:.1%} of buying power).\n"
                f"Exit Plan:\n"
                f"  - Take Profit Target: ${last_price * (1 + self.take_profit_pct):.2f} (+{self.take_profit_pct:.1%})\n"
                f"  - Stop Loss Target: ${last_price * (1 - self.stop_loss_pct):.2f} (-{self.stop_loss_pct:.1%})"
            )
            logging.info(message)
            await self.telegram_service.send_message(message)
            await manager.broadcast_json({"type": "log", "message": message})

            if notional_to_trade > 1.0: # Alpaca requires notional orders to be > $1
                order = self.alpaca_service.submit_order(
                    symbol=symbol,
                    notional=notional_to_trade,
                    side='buy',
                    type='market',
                    time_in_force='day', # Day order is safer for this strategy
                    order_class='bracket',
                    take_profit={'limit_price': round(last_price * (1 + self.take_profit_pct), 2)},
                    stop_loss={'stop_price': round(last_price * (1 - self.stop_loss_pct), 2)}
                )
                # Since we don't get immediate fill info on market orders, we'll log the submission.
                # A separate process should monitor fills.
                create_trade(
                    db, 
                    symbol=symbol, 
                    qty=order.qty or 0, 
                    price=order.filled_avg_price or last_price, # Use last_price as estimate
                    side=order.side, 
                    strategy='SMA Crossover',
                    entry_reason=f"Short SMA ({short_mavg:.2f}) crossed above Long SMA ({long_mavg:.2f})"
                )
                self.google_sheets_service.export_trades()

        elif latest_position == -1.0 and current_position_qty > 0:
            message = (
                f"TRADE SIGNAL: Sell {symbol}.\n"
                f"Reason: SMA Crossover (Short {self.short_window} SMA crossed below Long {self.long_window} SMA).\n"
                f"  - Short SMA: {short_mavg:.2f}\n"
                f"  - Long SMA: {long_mavg:.2f}\n"
                f"Closing position of {current_position_qty} shares."
            )
            logging.info(message)
            await self.telegram_service.send_message(message)
            await manager.broadcast_json({"type": "log", "message": message})
            
            # We cancel existing bracket orders and sell the full position
            self.alpaca_service.api.cancel_all_orders()
            order = self.alpaca_service.submit_order(
                symbol=symbol, 
                qty=current_position_qty, 
                side='sell', 
                type='market', 
                time_in_force='day'
            )
            create_trade(
                db, 
                symbol=symbol, 
                qty=order.qty or current_position_qty, 
                price=order.filled_avg_price or bars['close'].iloc[-1], # Estimate
                side=order.side, 
                strategy='SMA Crossover',
                entry_reason="", # Not an entry
                exit_reason=f"Short SMA ({short_mavg:.2f}) crossed below Long SMA ({long_mavg:.2f})"
            )
            self.google_sheets_service.export_trades()
        else:
            message = f"No signal for {symbol} or position is aligned with signal. Short SMA: {short_mavg:.2f}, Long SMA: {long_mavg:.2f}"
            logging.info(message)
            await manager.broadcast_json({"type": "log", "message": message})

    
