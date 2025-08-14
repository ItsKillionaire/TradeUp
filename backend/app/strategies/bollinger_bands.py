import logging
from sqlalchemy.orm import Session
from app.strategies.base import BaseStrategy
import pandas_ta as ta


class BollingerBandsStrategy(BaseStrategy):
    name: str = "bollinger_bands"
    display_name: str = "Bollinger Bands"
    description: str = "A volatility indicator that consists of a middle band (a simple moving average) and two outer bands that are typically two standard deviations away from the middle band."

    def __init__(self, *args, length=20, std_dev=2, **kwargs):
        super().__init__(*args, **kwargs)
        self.length = length
        self.std_dev = std_dev

    async def run(self, symbol, timeframe, db: Session):
        pass

    async def run_on_trade(self, trade):
        symbol = trade.symbol
        timeframe = "1Day"
        logging.info(f"Running Bollinger Bands strategy for {symbol}")

        bars = self.alpaca_service.get_bars(symbol, timeframe, limit=self.length + 5).df
        if bars.empty:
            return

        bars.ta.bbands(length=self.length, std=self.std_dev, append=True)

        latest_close = bars["close"].iloc[-1]
        lower_band = bars[f"BBL_{self.length}_{self.std_dev:.1f}"].iloc[-1]
        upper_band = bars[f"BBU_{self.length}_{self.std_dev:.1f}"].iloc[-1]

        if latest_close < lower_band:
            logging.info(f"Buy signal for {symbol} (Bollinger Bands)")
        elif latest_close > upper_band:
            logging.info(f"Sell signal for {symbol} (Bollinger Bands)")