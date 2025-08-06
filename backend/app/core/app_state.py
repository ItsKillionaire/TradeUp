
from app.core.strategy_manager import StrategyManager
from app.services.alpaca import AlpacaService
from app.services.telegram import TelegramService
from app.services.google_sheets import GoogleSheetsService

alpaca_service = AlpacaService()
telegram_service = TelegramService()
google_sheets_service = GoogleSheetsService()

strategy_manager = StrategyManager(
    alpaca_service=alpaca_service,
    telegram_service=telegram_service,
    google_sheets_service=google_sheets_service
)
