import logging
from sqlalchemy.orm import Session
from app.strategies.base import BaseStrategy
import pandas_ta as ta


class IchimokuCloudStrategy(BaseStrategy):
    name: str = "ichimoku_cloud"
    display_name: str = "Ichimoku Cloud"
    description: str = "A collection of indicators that show support and resistance levels, as well as momentum and trend direction."

    def __init__(self, *args, tenkan=9, kijun=26, senkou=52, **kwargs):
        super().__init__(*args, **kwargs)
        self.tenkan = tenkan
        self.kijun = kijun
        self.senkou = senkou

    async def run(self, symbol, timeframe, db: Session):
        pass

    async def run_on_trade(self, trade):
        symbol = trade.symbol
        timeframe = "1Day"
        logging.info(f"Running Ichimoku Cloud strategy for {symbol}")

        bars = self.alpaca_service.get_bars(
            symbol, timeframe, limit=self.senkou + 5
        ).df
        if bars.empty:
            return

        bars.ta.ichimoku(
            tenkan=self.tenkan, kijun=self.kijun, senkou=self.senkou, append=True
        )

        latest_close = bars["close"].iloc[-1]
        span_a = bars[f"ISA_{self.tenkan}_{self.kijun}_{self.senkou}"].iloc[-1]
        span_b = bars[f"ISB_{self.kijun}_{self.senkou}"].iloc[-1]

        if latest_close > span_a and latest_close > span_b:
            logging.info(f"Buy signal for {symbol} (Ichimoku Cloud)")
        elif latest_close < span_a and latest_close < span_b:
            logging.info(f"Sell signal for {symbol} (Ichimoku Cloud)")