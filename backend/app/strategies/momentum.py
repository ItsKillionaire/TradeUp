import logging
from sqlalchemy.orm import Session
from app.strategies.base import BaseStrategy
import pandas_ta as ta


class MomentumStrategy(BaseStrategy):
    name: str = "momentum"
    display_name: str = "Momentum"
    description: str = "A strategy that aims to capitalize on the continuance of existing trends in the market."

    def __init__(self, *args, momentum_period=14, **kwargs):
        super().__init__(*args, **kwargs)
        self.momentum_period = momentum_period

    async def run(self, symbol, timeframe, db: Session):
        pass

    async def run_on_trade(self, trade):
        symbol = trade.symbol
        timeframe = "1Day"
        logging.info(f"Running Momentum strategy for {symbol}")

        bars = self.alpaca_service.get_bars(
            symbol, timeframe, limit=self.momentum_period + 5
        ).df
        if bars.empty:
            return

        bars["momentum"] = bars["close"].diff(self.momentum_period)

        latest_momentum = bars["momentum"].iloc[-1]

        if latest_momentum > 0:
            logging.info(f"Buy signal for {symbol} (Momentum)")
        elif latest_momentum < 0:
            logging.info(f"Sell signal for {symbol} (Momentum)")