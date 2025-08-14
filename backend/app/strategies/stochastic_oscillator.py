import logging
from sqlalchemy.orm import Session
from app.strategies.base import BaseStrategy
import pandas_ta as ta


class StochasticOscillatorStrategy(BaseStrategy):
    name: str = "stochastic_oscillator"
    display_name: str = "Stochastic Oscillator"
    description: str = "A momentum indicator that compares a particular closing price of a security to a range of its prices over a certain period of time."

    def __init__(self, *args, k_period=14, d_period=3, overbought=80, oversold=20, **kwargs):
        super().__init__(*args, **kwargs)
        self.k_period = k_period
        self.d_period = d_period
        self.overbought = overbought
        self.oversold = oversold

    async def run(self, symbol, timeframe, db: Session):
        pass

    async def run_on_trade(self, trade):
        symbol = trade.symbol
        timeframe = "1Day"
        logging.info(f"Running Stochastic Oscillator strategy for {symbol}")

        bars = self.alpaca_service.get_bars(
            symbol, timeframe, limit=self.k_period + self.d_period
        ).df
        if bars.empty:
            return

        bars.ta.stoch(
            k=self.k_period, d=self.d_period, append=True
        )

        latest_k = bars[f"STOCHk_{self.k_period}_{self.d_period}_3"].iloc[-1]
        latest_d = bars[f"STOCHd_{self.k_period}_{self.d_period}_3"].iloc[-1]

        if latest_k > self.overbought and latest_d > self.overbought:
            logging.info(f"Sell signal for {symbol} (Stochastic Oscillator > {self.overbought})")
        elif latest_k < self.oversold and latest_d < self.oversold:
            logging.info(f"Buy signal for {symbol} (Stochastic Oscillator < {self.oversold})")

    def generate_signals(self, bars):
        if bars.empty:
            return bars

        bars.ta.stoch(
            k=self.k_period, d=self.d_period, append=True
        )

        k_col = f"STOCHk_{self.k_period}_{self.d_period}_3"
        d_col = f"STOCHd_{self.k_period}_{self.d_period}_3"

        bars["signal"] = 0
        bars.loc[(bars[k_col] < self.oversold) & (bars[d_col] < self.oversold), "signal"] = 1
        bars.loc[(bars[k_col] > self.overbought) & (bars[d_col] > self.overbought), "signal"] = -1

        return bars