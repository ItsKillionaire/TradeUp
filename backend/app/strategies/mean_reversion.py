import logging
from sqlalchemy.orm import Session
from app.strategies.base import BaseStrategy
import pandas_ta as ta


class MeanReversionStrategy(BaseStrategy):
    name: str = "mean_reversion"
    display_name: str = "Mean Reversion"
    description: str = "A strategy that assumes that a stock's price will tend to move back to the average price over time."

    def __init__(self, *args, sma_period=20, deviation_threshold=2, **kwargs):
        super().__init__(*args, **kwargs)
        self.sma_period = sma_period
        self.deviation_threshold = deviation_threshold

    async def run(self, symbol, timeframe, db: Session):
        pass

    async def run_on_trade(self, trade):
        symbol = trade.symbol
        timeframe = "1Day"
        logging.info(f"Running Mean Reversion strategy for {symbol}")

        bars = self.alpaca_service.get_bars(
            symbol, timeframe, limit=self.sma_period + 5
        ).df
        if bars.empty:
            return

        bars.ta.sma(length=self.sma_period, append=True)
        bars["std_dev"] = bars["close"].rolling(window=self.sma_period).std()

        latest_close = bars["close"].iloc[-1]
        sma = bars[f"SMA_{self.sma_period}"].iloc[-1]
        std_dev = bars["std_dev"].iloc[-1]

        if latest_close < sma - (self.deviation_threshold * std_dev):
            logging.info(f"Buy signal for {symbol} (Mean Reversion)")
        elif latest_close > sma + (self.deviation_threshold * std_dev):
            logging.info(f"Sell signal for {symbol} (Mean Reversion)")

    def generate_signals(self, bars):
        if bars.empty:
            return bars

        bars.ta.sma(length=self.sma_period, append=True)
        bars["std_dev"] = bars["close"].rolling(window=self.sma_period).std()

        sma_col = f"SMA_{self.sma_period}"

        bars["signal"] = 0
        bars.loc[bars["close"] < bars[sma_col] - (self.deviation_threshold * bars["std_dev"]), "signal"] = 1
        bars.loc[bars["close"] > bars[sma_col] + (self.deviation_threshold * bars["std_dev"]), "signal"] = -1

        return bars