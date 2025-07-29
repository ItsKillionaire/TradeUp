from app.strategies.base import BaseStrategy
from app.strategies.sma_crossover import SmaCrossover
from app.strategies.adaptive_strategy import AdaptiveStrategy

class StrategyManager:
    def __init__(self, alpaca_service):
        self.strategies = {
            "sma_crossover": SmaCrossover(alpaca_service),
            "adaptive_strategy": AdaptiveStrategy(alpaca_service),
            # Add other strategies here
        }

    def get_strategy(self, name: str) -> BaseStrategy:
        return self.strategies.get(name)

    def get_available_strategies(self):
        return list(self.strategies.keys())
