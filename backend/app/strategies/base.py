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
        raise NotImplementedError(
            "Each strategy must implement its own generate_signals method for backtesting."
        )

    def get_name(self):
        return self.name


def get_strategy(name, *args, **kwargs):
    from .sma_crossover import SmaCrossover
    from .mean_reversion import MeanReversion
    from .ai_strategy import AIStrategy

    strategies = {
        "SMA Crossover": SmaCrossover,
        "Mean Reversion": MeanReversion,
        "AI Strategy": AIStrategy,
    }

    strategy_class = strategies.get(name)
    if strategy_class:
        from ..services.alpaca import AlpacaService
        from ..services.telegram import TelegramService
        from ..services.google_sheets import GoogleSheetsService

        alpaca_service = AlpacaService()
        telegram_service = TelegramService()
        google_sheets_service = GoogleSheetsService()

        try:
            account_info = alpaca_service.api.get_account()
            risk_manager = RiskManager(account_equity=float(account_info.equity))
        except Exception as e:
            logging.error(
                f"Failed to initialize RiskManager: {e}. Defaulting to a fixed equity of 100,000."
            )
            risk_manager = RiskManager(account_equity=100000)

        return strategy_class(
            alpaca_service,
            risk_manager,
            telegram_service,
            google_sheets_service,
            *args,
            **kwargs,
        )
    return None
