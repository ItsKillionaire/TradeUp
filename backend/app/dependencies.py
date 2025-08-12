from app.services.alpaca import AlpacaService
from app.services.telegram import TelegramService
from app.services.google_sheets import GoogleSheetsService

_alpaca_service_instance = None

def get_alpaca_service():
    global _alpaca_service_instance
    if _alpaca_service_instance is None:
        _alpaca_service_instance = AlpacaService()
    return _alpaca_service_instance

def get_telegram_service():
    return TelegramService()

def get_google_sheets_service():
    return GoogleSheetsService()
