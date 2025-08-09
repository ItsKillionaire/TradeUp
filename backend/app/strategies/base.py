from abc import ABC, abstractmethod
from app.services.alpaca import AlpacaService
import logging

class BaseStrategy(ABC):
    def __init__(self, alpaca_service: AlpacaService, name: str):
        self.alpaca_service = alpaca_service
        self.name = name

    def run(self, symbol: str, timeframe: str):
        pass

    def run_on_trade(self, trade):
        pass

    async def get_position(self, symbol: str) -> float:
        try:
            position = await self.alpaca_service.api.get_position(symbol)
            return float(position.qty)
        except Exception as e:
            logging.warning(f"Could not get position for {symbol}: {e}")
            return 0.0
