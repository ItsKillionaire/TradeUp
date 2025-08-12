from abc import ABC, abstractmethod
from app.services.alpaca import AlpacaService
import logging

class BaseStrategy:
    def __init__(self, alpaca_service, name="Base Strategy"):
        self.alpaca_service = alpaca_service
        self.name = name
        logging.info(f"{self.name} strategy initialized.")

    async def run(self, symbol, timeframe, db_session):
        raise NotImplementedError("Each strategy must implement its own run method.")

    def generate_signals(self, bars):
        """
        Generates trading signals for backtesting.
        This method should be implemented by each strategy.

        :param bars: A pandas DataFrame with historical market data (OHLCV).
        :return: A pandas DataFrame with a 'position' column containing signals (1, 0, -1).
        """
        raise NotImplementedError("Each strategy must implement its own generate_signals method for backtesting.")

    def get_name(self):
        return self.name

# This function is a factory for strategies.
def get_strategy(name, *args, **kwargs):
    # This is a bit of a hack to avoid circular imports
    # A better solution might be a registration pattern.
    from .sma_crossover import SmaCrossover
    from .mean_reversion import MeanReversion
    # ... import other strategies here

    strategies = {
        "SMA Crossover": SmaCrossover,
        "Mean Reversion": MeanReversion,
        # ... add other strategies here
    }
    
    strategy_class = strategies.get(name)
    if strategy_class:
        # This is a placeholder for proper dependency injection
        from ..services.alpaca import AlpacaService
        from ..services.telegram import TelegramService
        from ..services.google_sheets import GoogleSheetsService
        
        # These should be singletons or provided by a DI container
        alpaca_service = AlpacaService()
        telegram_service = TelegramService()
        google_sheets_service = GoogleSheetsService()

        return strategy_class(alpaca_service, telegram_service, google_sheets_service, *args, **kwargs)
    return None

