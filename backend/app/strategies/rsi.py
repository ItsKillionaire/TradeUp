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


class RsiStrategy(BaseStrategy):
    def __init__(
        self,
        alpaca_service,
        telegram_service,
        google_sheets_service,
        rsi_period=14,
        rsi_oversold=30,
        rsi_overbought=70,
        trade_percentage=0.05,
        take_profit_pct=0.05,
        stop_loss_pct=0.02,
    ):
        super().__init__(alpaca_service)
        self.rsi_period = rsi_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
        self.trade_percentage = trade_percentage
        self.take_profit_pct = take_profit_pct
        self.stop_loss_pct = stop_loss_pct
        self.telegram_service = telegram_service
        self.google_sheets_service = google_sheets_service

    async def run(self, symbol, timeframe, db: Session):
        logging.info(f"Running RSI strategy for {symbol}")

        bars = self.alpaca_service.get_bars(
            symbol, timeframe, limit=self.rsi_period + 5
        ).df
        logging.info(
            f"Fetched {len(bars)} bars for {symbol} with timeframe {timeframe}."
        )

        if len(bars) < self.rsi_period:
            logging.warning(f"Not enough data for {symbol} to run strategy.")
            return

        bars.ta.rsi(length=self.rsi_period, append=True)

        latest_rsi = bars[f"RSI_{self.rsi_period}"].iloc[-1]
        logging.info(f"Latest RSI for {symbol}: {latest_rsi}")

        current_position = await self.get_position(symbol)

        if latest_rsi < self.rsi_oversold and current_position == 0:
            message = f"Buy signal for {symbol} (RSI: {latest_rsi:.2f})"
            logging.info(message)
            await self.telegram_service.send_message(message)
            await manager.broadcast_json({"type": "log", "message": message})

            account_info = await self.alpaca_service.get_account_info()
            buying_power = float(account_info.buying_power)
            last_price = bars["close"].iloc[-1]
            qty = int((buying_power * self.trade_percentage) / last_price)

            if qty > 0:
                order = self.alpaca_service.submit_order(
                    symbol=symbol,
                    qty=qty,
                    side="buy",
                    type="market",
                    time_in_force="gtc",
                    order_class="bracket",
                    take_profit={
                        "limit_price": last_price * (1 + self.take_profit_pct)
                    },
                    stop_loss={"stop_price": last_price * (1 - self.stop_loss_pct)},
                )
                create_trade(db, symbol, order.qty, order.filled_avg_price, order.side)
                self.google_sheets_service.export_trades()
        elif latest_rsi > self.rsi_overbought and current_position > 0:
            message = f"Sell signal for {symbol} (RSI: {latest_rsi:.2f})"
            logging.info(message)
            await self.telegram_service.send_message(message)
            await manager.broadcast_json({"type": "log", "message": message})
            order = self.alpaca_service.submit_order(
                symbol, current_position, "sell", "market", "gtc"
            )
            create_trade(db, symbol, order.qty, order.filled_avg_price, order.side)
            self.google_sheets_service.export_trades()
        else:
            message = (
                f"No signal for {symbol} (RSI: {latest_rsi:.2f}) or already in position"
            )
            logging.info(message)
            await manager.broadcast_json({"type": "log", "message": message})
