from app.strategies.base import BaseStrategy
from app.strategies.sma_crossover import SmaCrossover
from app.strategies.adaptive_strategy import AdaptiveStrategy
from app.strategies.rsi import RsiStrategy
from app.strategies.macd import MacdStrategy
from app.strategies.bollinger_bands import BollingerBandsStrategy
from app.strategies.ema_crossover import EmaCrossoverStrategy
from app.strategies.stochastic_oscillator import StochasticOscillatorStrategy
from app.strategies.ichimoku_cloud import IchimokuCloudStrategy
from app.strategies.vwap import VwapStrategy
from app.strategies.mean_reversion import MeanReversionStrategy
from app.strategies.momentum import MomentumStrategy
from app.strategies.awesome_oscillator import AwesomeOscillatorStrategy
from typing import Dict, Type, Any
from sqlalchemy.orm import Session

class StrategyManager:
    def __init__(self, alpaca_service, telegram_service, google_sheets_service):
        self.alpaca_service = alpaca_service
        self.telegram_service = telegram_service
        self.google_sheets_service = google_sheets_service
        self.active_strategies = []
        self.alpaca_service = alpaca_service
        self.telegram_service = telegram_service
        self.google_sheets_service = google_sheets_service
        self._strategy_classes: Dict[str, Dict[str, Any]] = {
            "sma_crossover": {
                "class": SmaCrossover,
                "display_name": "SMA Crossover",
                "description": "A simple strategy that generates buy/sell signals based on the crossover of two Simple Moving Averages (SMAs) of different lengths."
            },
            "adaptive_strategy": {
                "class": AdaptiveStrategy,
                "display_name": "Adaptive Strategy",
                "description": "A strategy that adapts to changing market conditions by adjusting its parameters based on market volatility."
            },
            "rsi": {
                "class": RsiStrategy,
                "display_name": "RSI",
                "description": "A momentum oscillator that measures the speed and change of price movements. It is used to identify overbought or oversold conditions."
            },
            "macd": {
                "class": MacdStrategy,
                "display_name": "MACD",
                "description": "A trend-following momentum indicator that shows the relationship between two moving averages of a security's price."
            },
            "bollinger_bands": {
                "class": BollingerBandsStrategy,
                "display_name": "Bollinger Bands",
                "description": "A volatility indicator that consists of a middle band (a simple moving average) and two outer bands that are typically two standard deviations away from the middle band."
            },
            "ema_crossover": {
                "class": EmaCrossoverStrategy,
                "display_name": "EMA Crossover",
                "description": "Similar to the SMA Crossover, but uses Exponential Moving Averages (EMAs) which give more weight to recent prices."
            },
            "stochastic_oscillator": {
                "class": StochasticOscillatorStrategy,
                "display_name": "Stochastic Oscillator",
                "description": "A momentum indicator that compares a particular closing price of a security to a range of its prices over a certain period of time."
            },
            "ichimoku_cloud": {
                "class": IchimokuCloudStrategy,
                "display_name": "Ichimoku Cloud",
                "description": "A collection of indicators that show support and resistance levels, as well as momentum and trend direction."
            },
            "vwap": {
                "class": VwapStrategy,
                "display_name": "VWAP",
                "description": "Volume-Weighted Average Price (VWAP) is a trading benchmark that gives the average price a security has traded at throughout the day, based on both volume and price."
            },
            "mean_reversion": {
                "class": MeanReversionStrategy,
                "display_name": "Mean Reversion",
                "description": "A strategy that assumes that a stock's price will tend to move back to the average price over time."
            },
            "momentum": {
                "class": MomentumStrategy,
                "display_name": "Momentum",
                "description": "A strategy that aims to capitalize on the continuance of existing trends in the market."
            },
            "awesome_oscillator": {
                "class": AwesomeOscillatorStrategy,
                "display_name": "Awesome Oscillator",
                "description": "An indicator used to measure market momentum. It is calculated as the difference between a 34-period and a 5-period simple moving average."
            }
        }

    def get_strategy_instance(self, name: str, **kwargs) -> BaseStrategy:
        strategy_info = self._strategy_classes.get(name)
        if not strategy_info:
            return None
        strategy_class = strategy_info["class"]
        return strategy_class(
            self.alpaca_service,
            self.telegram_service,
            self.google_sheets_service,
            **kwargs
        )

    def get_available_strategies(self):
        return [
            {
                "name": name,
                "display_name": info["display_name"],
                "description": info["description"]
            }
            for name, info in self._strategy_classes.items()
        ]

    async def run_strategy(self, name: str, symbol: str, timeframe: str, db: Session, strategy_params: Dict[str, Any]):
        strategy_instance = self.get_strategy_instance(name, symbol=symbol, timeframe=timeframe, **strategy_params)
        if strategy_instance:
            self.active_strategies.append(strategy_instance)
            await strategy_instance.run(db)
        else:
            raise ValueError(f"Strategy '{name}' not found.")

    async def run_strategy_on_trade(self, trade):
        for strategy in self.active_strategies:
            if strategy.symbol == trade.symbol:
                await strategy.run_on_trade(trade)
