from abc import ABC, abstractmethod
from app.services.alpaca import AlpacaService
import logging
from ..core.risk_manager import RiskManager

class BaseStrategy:
    def __init__(self, alpaca_service, risk_manager, name="Base Strategy"):
        self.alpaca_service = alpaca_service
        self.risk_manager = risk_manager
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
    from .ai_strategy import AIStrategy
    # ... import other strategies here

    strategies = {
        "SMA Crossover": SmaCrossover,
        "Mean Reversion": MeanReversion,
        "AI Strategy": AIStrategy,
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

        # Create RiskManager
        try:
            # This is a blocking call, which is not ideal in an async context.
            # In a real application, the account info might be cached or fetched asynchronously.
            account_info = alpaca_service.api.get_account()
            risk_manager = RiskManager(account_equity=float(account_info.equity))
        except Exception as e:
            logging.error(f"Failed to initialize RiskManager: {e}. Defaulting to a fixed equity of 100,000.")
            risk_manager = RiskManager(account_equity=100000)


        return strategy_class(alpaca_service, risk_manager, telegram_service, google_sheets_service, *args, **kwargs)
    return None

