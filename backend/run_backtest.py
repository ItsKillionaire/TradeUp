import asyncio
from app.backtester.backtester import Backtester
from app.services.alpaca import AlpacaService
from app.strategies.sma_crossover import SmaCrossover
from app.core.risk_manager import RiskManager
from app.services.telegram import TelegramService
from app.services.google_sheets import GoogleSheetsService
from config import settings
import json


async def main():
    # Note: This is a simplified setup for backtesting.
    # In a real application, you would have a more robust way to manage services.
    alpaca_service = AlpacaService()
    risk_manager = RiskManager(account_equity=100000)  # Initial capital for backtest

    # These services are not used in the backtest, so we can pass None or mock objects
    telegram_service = None
    google_sheets_service = None

    strategy = SmaCrossover(
        alpaca_service=alpaca_service,
        risk_manager=risk_manager,
        telegram_service=telegram_service,
        google_sheets_service=google_sheets_service,
    )

    backtester = Backtester(
        alpaca_service=alpaca_service,
        strategy=strategy,
        start_date="2022-01-01",
        end_date="2023-01-01",
        initial_capital=100000,
    )

    results = backtester.run(symbol="SPY")

    print("Backtest Results:")
    print(json.dumps(results, indent=4))


if __name__ == "__main__":
    asyncio.run(main())
