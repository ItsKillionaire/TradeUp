from abc import ABC, abstractmethod
from app.services.alpaca import AlpacaService

class BaseStrategy(ABC):
    def __init__(self, alpaca_service: AlpacaService):
        self.alpaca_service = alpaca_service

    @abstractmethod
    def run(self, symbol: str, timeframe: str):
        pass
