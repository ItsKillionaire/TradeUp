import logging
from sqlalchemy.orm import Session
from app.strategies.base import BaseStrategy
import pandas_ta as ta


class MacdStrategy(BaseStrategy):
    name: str = "macd"
    display_name: str = "MACD"
    description: str = "A trend-following momentum indicator that shows the relationship between two moving averages of a security's price."

    def __init__(self, *args, fast=12, slow=26, signal=9, **kwargs):
        super().__init__(*args, **kwargs)
        self.fast = fast
        self.slow = slow
        self.signal = signal

    async def run(self, symbol, timeframe, db: Session):
        pass

    async def run_on_trade(self, trade):
        symbol = trade.symbol
        timeframe = "1Day"
        logging.info(f"Running MACD strategy for {symbol}")

        bars = self.alpaca_service.get_bars(
            symbol, timeframe, limit=self.slow + self.signal
        ).df
        if bars.empty:
            return

        bars.ta.macd(
            fast=self.fast, slow=self.slow, signal=self.signal, append=True
        )

        latest_macd = bars[f"MACD_{self.fast}_{self.slow}_{self.signal}"].iloc[-1]
        latest_signal = bars[f"MACDs_{self.fast}_{self.slow}_{self.signal}"].iloc[-1]
        previous_macd = bars[f"MACD_{self.fast}_{self.slow}_{self.signal}"].iloc[-2]
        previous_signal = bars[f"MACDs_{self.fast}_{self.slow}_{self.signal}"].iloc[-2]

        if latest_macd > latest_signal and previous_macd <= previous_signal:
            logging.info(f"Buy signal for {symbol} (MACD)")
        elif latest_macd < latest_signal and previous_macd >= previous_signal:
            logging.info(f"Sell signal for {symbol} (MACD)")

    def generate_signals(self, bars):
        if bars.empty:
            return bars

        bars.ta.macd(
            fast=self.fast, slow=self.slow, signal=self.signal, append=True
        )

        macd_col = f"MACD_{self.fast}_{self.slow}_{self.signal}"
        signal_col = f"MACDs_{self.fast}_{self.slow}_{self.signal}"

        bars["signal"] = 0
        bars.loc[(bars[macd_col] > bars[signal_col]) & (bars[macd_col].shift(1) <= bars[signal_col].shift(1)), "signal"] = 1
        bars.loc[(bars[macd_col] < bars[signal_col]) & (bars[macd_col].shift(1) >= bars[signal_col].shift(1)), "signal"] = -1

        return bars