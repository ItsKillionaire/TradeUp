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
        self._strategy_classes: Dict[str, Type[BaseStrategy]] = {
            "sma_crossover": SmaCrossover,
            "adaptive_strategy": AdaptiveStrategy,
            "rsi": RsiStrategy,
            "macd": MacdStrategy,
            "bollinger_bands": BollingerBandsStrategy,
            "ema_crossover": EmaCrossoverStrategy,
            "stochastic_oscillator": StochasticOscillatorStrategy,
            "ichimoku_cloud": IchimokuCloudStrategy,
            "vwap": VwapStrategy,
            "mean_reversion": MeanReversionStrategy,
            "momentum": MomentumStrategy,
            "awesome_oscillator": AwesomeOscillatorStrategy,
        }

    def get_strategy_instance(self, name: str, **kwargs) -> BaseStrategy:
        strategy_class = self._strategy_classes.get(name)
        if not strategy_class:
            return None
        return strategy_class(
            self.alpaca_service, 
            self.telegram_service, 
            self.google_sheets_service, 
            **kwargs
        )

    def get_available_strategies(self):
        return list(self._strategy_classes.keys())

    async def run_strategy(self, name: str, symbol: str, timeframe: str, db: Session, strategy_params: Dict[str, Any]):
        strategy_instance = self.get_strategy_instance(name, **strategy_params)
        if strategy_instance:
            await strategy_instance.run(symbol, timeframe, db)
        else:
            raise ValueError(f"Strategy '{name}' not found.")
