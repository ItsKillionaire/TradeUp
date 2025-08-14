from abc import ABC, abstractmethod
from app.services.alpaca import AlpacaService
import logging
from ..core.risk_manager import RiskManager


class BaseStrategy(ABC):
    name: str = "Base Strategy"
    display_name: str = "Base Strategy"
    description: str = "A base strategy template."

    def __init__(
        self,
        alpaca_service: AlpacaService,
        risk_manager: RiskManager,
        telegram_service,
        google_sheets_service,
        symbol: str = None,
        **kwargs,
    ):
        self.alpaca_service = alpaca_service
        self.risk_manager = risk_manager
        self.telegram_service = telegram_service
        self.google_sheets_service = google_sheets_service
        self.symbol = symbol
        logging.info(f"{self.name} strategy initialized for symbol {self.symbol}.")

    @abstractmethod
    async def run(self, symbol, timeframe, db_session):
        raise NotImplementedError("Each strategy must implement its own run method.")

    @abstractmethod
    def generate_signals(self, bars):
        raise NotImplementedError(
            "Each strategy must implement its own generate_signals method for backtesting."
        )
