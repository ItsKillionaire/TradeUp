import logging
from sqlalchemy.orm import Session
from app.strategies.base import BaseStrategy
import pandas_ta as ta


class EmaCrossoverStrategy(BaseStrategy):
    name: str = "ema_crossover"
    display_name: str = "EMA Crossover"
    description: str = "Similar to the SMA Crossover, but uses Exponential Moving Averages (EMAs) which give more weight to recent prices."

    def __init__(self, *args, fast_period=12, slow_period=26, **kwargs):
        super().__init__(*args, **kwargs)
        self.fast_period = fast_period
        self.slow_period = slow_period

    async def run(self, symbol, timeframe, db: Session):
        pass

    async def run_on_trade(self, trade):
        symbol = trade.symbol
        timeframe = "1Day"
        logging.info(f"Running EMA Crossover strategy for {symbol}")

        bars = self.alpaca_service.get_bars(
            symbol, timeframe, limit=self.slow_period + 5
        ).df
        if bars.empty:
            return

        bars.ta.ema(length=self.fast_period, append=True)
        bars.ta.ema(length=self.slow_period, append=True)

        latest_fast_ema = bars[f"EMA_{self.fast_period}"].iloc[-1]
        latest_slow_ema = bars[f"EMA_{self.slow_period}"].iloc[-1]
        previous_fast_ema = bars[f"EMA_{self.fast_period}"].iloc[-2]
        previous_slow_ema = bars[f"EMA_{self.slow_period}"].iloc[-2]

        if latest_fast_ema > latest_slow_ema and previous_fast_ema <= previous_slow_ema:
            logging.info(f"Buy signal for {symbol} (EMA Crossover)")
        elif latest_fast_ema < latest_slow_ema and previous_fast_ema >= previous_slow_ema:
            logging.info(f"Sell signal for {symbol} (EMA Crossover)")