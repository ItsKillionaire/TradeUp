import logging
import pandas as pd
import pandas_ta as ta
from sqlalchemy.orm import Session
from app.strategies.base import BaseStrategy
from app.services.telegram import TelegramService
from app.services.google_sheets import GoogleSheetsService
from app.crud import create_trade
from app.core.connection_manager import manager


class SmaCrossover(BaseStrategy):
    name: str = "sma_crossover"
    display_name: str = "SMA Crossover"
    description: str = "A simple strategy that generates buy/sell signals based on the crossover of two Simple Moving Averages (SMAs) of different lengths."

    def __init__(
        self,
        *args,
        fast_period=10,
        slow_period=30,
        trade_percentage=0.05,
        take_profit_pct=0.05,
        stop_loss_pct=0.02,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.trade_percentage = trade_percentage
        self.take_profit_pct = take_profit_pct
        self.stop_loss_pct = stop_loss_pct

    async def get_position(self, symbol: str) -> float:
        try:
            position = await self.alpaca_service.api.get_position(symbol)
            return float(position.qty)
        except Exception as e:
            logging.warning(f"Could not get position for {symbol}: {e}")
            return 0.0

    async def run(self, symbol, timeframe, db: Session):
        pass

    async def run_on_trade(self, trade):
        symbol = trade.symbol
        timeframe = "1Day"
        logging.info(f"Running SMA Crossover strategy for {symbol}")

        bars = self.alpaca_service.get_bars(
            symbol, timeframe, limit=self.slow_period + 5
        ).df
        logging.info(
            f"Fetched {len(bars)} bars for {symbol} with timeframe {timeframe}."
        )

        if len(bars) < self.slow_period:
            logging.warning(f"Not enough data for {symbol} to run strategy.")
            return

        bars.ta.sma(length=self.fast_period, append=True)
        bars.ta.sma(length=self.slow_period, append=True)

        latest_fast_sma = bars[f"SMA_{self.fast_period}"].iloc[-1]
        latest_slow_sma = bars[f"SMA_{self.slow_period}"].iloc[-1]
        previous_fast_sma = bars[f"SMA_{self.fast_period}"].iloc[-2]
        previous_slow_sma = bars[f"SMA_{self.slow_period}"].iloc[-2]

        logging.info(
            f"Latest fast SMA for {symbol}: {latest_fast_sma:.2f}, slow SMA: {latest_slow_sma:.2f}"
        )

        current_position = await self.get_position(symbol)

        if (
            latest_fast_sma > latest_slow_sma
            and previous_fast_sma < previous_slow_sma
            and current_position == 0
        ):
            message = f"Buy signal for {symbol} (SMA Crossover)"
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

        elif (
            latest_fast_sma < latest_slow_sma
            and previous_fast_sma > previous_slow_sma
            and current_position > 0
        ):
            message = f"Sell signal for {symbol} (SMA Crossover)"
            logging.info(message)
            await self.telegram_service.send_message(message)
            await manager.broadcast_json({"type": "log", "message": message})
            order = self.alpaca_service.submit_order(
                symbol, current_position, "sell", "market", "gtc"
            )
            create_trade(db, symbol, order.qty, order.filled_avg_price, order.side)
            self.google_sheets_service.export_trades()
        else:
            message = f"No signal for {symbol} (SMA Crossover) or already in position"
            logging.info(message)
            await manager.broadcast_json({"type": "log", "message": message})