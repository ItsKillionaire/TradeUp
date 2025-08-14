import logging
import pkgutil
import inspect
from app.strategies.base import BaseStrategy
import app.strategies
from typing import Dict, Type, Any
from sqlalchemy.orm import Session


class StrategyManager:
    def __init__(
        self, alpaca_service, risk_manager, telegram_service, google_sheets_service
    ):
        self.alpaca_service = alpaca_service
        self.risk_manager = risk_manager
        self.telegram_service = telegram_service
        self.google_sheets_service = google_sheets_service
        self.active_strategies = []
        self._strategy_classes = self._discover_strategies()
        logging.info(f"Discovered {len(self._strategy_classes)} strategies.")

    def _discover_strategies(self) -> Dict[str, Dict[str, Any]]:
        strategies = {}
        for importer, modname, ispkg in pkgutil.iter_modules(app.strategies.__path__):
            if not ispkg and modname != "base":
                module = __import__(f"app.strategies.{modname}", fromlist="dummy")
                for name, obj in inspect.getmembers(module):
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, BaseStrategy)
                        and obj is not BaseStrategy
                    ):
                        strategies[obj.name] = {
                            "class": obj,
                            "display_name": obj.display_name,
                            "description": obj.description,
                        }
        return strategies

    def get_strategy_instance(self, name: str, **kwargs) -> BaseStrategy:
        strategy_info = self._strategy_classes.get(name)
        if not strategy_info:
            return None
        strategy_class = strategy_info["class"]
        logging.info(f"Instantiating strategy {name} with kwargs: {kwargs}")
        return strategy_class(
            self.alpaca_service,
            self.risk_manager,
            self.telegram_service,
            self.google_sheets_service,
            **kwargs,
        )

    def get_available_strategies(self):
        return [
            {
                "name": name,
                "display_name": info["display_name"],
                "description": info["description"],
            }
            for name, info in self._strategy_classes.items()
        ]

    async def run_strategy(
        self,
        name: str,
        symbol: str,
        timeframe: str,
        db: Session,
        strategy_params: Dict[str, Any],
    ):
        strategy_instance = self.get_strategy_instance(name, **strategy_params)
        if strategy_instance:
            self.active_strategies.append(strategy_instance)
            await strategy_instance.run(symbol, timeframe, db)
        else:
            raise ValueError(f"Strategy '{name}' not found.")

    async def run_strategy_on_trade(self, trade):
        for strategy in self.active_strategies:
            if strategy.symbol == trade.symbol:
                await strategy.run_on_trade(trade)