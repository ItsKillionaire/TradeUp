import logging
from sqlalchemy.orm import Session
from app.strategies.base import BaseStrategy
import pandas_ta as ta


class VwapStrategy(BaseStrategy):
    name: str = "vwap"
    display_name: str = "VWAP"
    description: str = "Volume-Weighted Average Price (VWAP) is a trading benchmark that gives the average price a security has traded at throughout the day, based on both volume and price."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def run(self, symbol, timeframe, db: Session):
        pass

    async def run_on_trade(self, trade):
        symbol = trade.symbol
        timeframe = "1Day"
        logging.info(f"Running VWAP strategy for {symbol}")

        bars = self.alpaca_service.get_bars(symbol, timeframe, limit=2).df
        if bars.empty:
            return

        bars.ta.vwap(append=True)

        latest_close = bars["close"].iloc[-1]
        latest_vwap = bars["VWAP_D"].iloc[-1]

        if latest_close > latest_vwap:
            logging.info(f"Buy signal for {symbol} (VWAP)")
        elif latest_close < latest_vwap:
            logging.info(f"Sell signal for {symbol} (VWAP)")

    def generate_signals(self, bars):
        if bars.empty:
            return bars

        bars.ta.vwap(append=True)

        vwap_col = "VWAP_D"

        bars["signal"] = 0
        bars.loc[bars["close"] > bars[vwap_col], "signal"] = 1
        bars.loc[bars["close"] < bars[vwap_col], "signal"] = -1

        return bars