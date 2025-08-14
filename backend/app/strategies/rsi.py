import logging
from sqlalchemy.orm import Session
from app.strategies.base import BaseStrategy
import pandas_ta as ta


class RsiStrategy(BaseStrategy):
    name: str = "rsi"
    display_name: str = "RSI"
    description: str = "A momentum oscillator that measures the speed and change of price movements. It is used to identify overbought or oversold conditions."

    def __init__(self, *args, period=14, overbought=70, oversold=30, **kwargs):
        super().__init__(*args, **kwargs)
        self.period = period
        self.overbought = overbought
        self.oversold = oversold

    async def run(self, symbol, timeframe, db: Session):
        pass

    async def run_on_trade(self, trade):
        symbol = trade.symbol
        timeframe = "1Day"
        logging.info(f"Running RSI strategy for {symbol}")

        bars = self.alpaca_service.get_bars(
            symbol, timeframe, limit=self.period + 5
        ).df
        if bars.empty:
            return

        bars.ta.rsi(length=self.period, append=True)

        latest_rsi = bars[f"RSI_{self.period}"].iloc[-1]

        if latest_rsi > self.overbought:
            logging.info(f"Sell signal for {symbol} (RSI > {self.overbought})")
        elif latest_rsi < self.oversold:
            logging.info(f"Buy signal for {symbol} (RSI < {self.oversold})")