import pytest
from unittest.mock import AsyncMock, MagicMock
from pytest_mock import MockerFixture
import pandas as pd
from app.core.database import SessionLocal
import sys


@pytest.fixture
def mock_alpaca_service():
    service = MagicMock()
    service.api = MagicMock()
    service.get_account_info = AsyncMock(return_value=MagicMock(buying_power="10000"))
    return service

@pytest.fixture(scope="session")
def mock_telegram_service():
    service = MagicMock()
    service.send_message = AsyncMock()
    return service

@pytest.fixture(scope="session")
def mock_google_sheets_service():
    service = MagicMock()
    service.export_trades = MagicMock()
    return service

@pytest.fixture
def mock_db_session():
    db = MagicMock(spec=SessionLocal)
    return db

@pytest.fixture(scope="session", autouse=True)
def mock_config_and_models(session_mocker: MockerFixture, mock_telegram_service, mock_google_sheets_service):
    # Create a mock for the config module
    mock_config = MagicMock()
    mock_config.settings.ALPACA_API_KEY = "test_key"
    mock_config.settings.ALPACA_SECRET_KEY = "test_secret"
    mock_config.settings.ALPACA_BASE_URL = "https://test-api.alpaca.markets"
    mock_config.settings.TELEGRAM_BOT_TOKEN = "test_token"
    mock_config.settings.TELEGRAM_CHAT_ID = "test_chat_id"
    mock_config.settings.GOOGLE_SHEETS_CREDENTIALS = "{}"

    # Patch sys.modules to return our mock_config when 'config' is imported
    session_mocker.patch.dict(sys.modules, {'config': mock_config})

    # Patch app.models.trade.Trade to prevent SQLAlchemy re-registration issues
    session_mocker.patch.dict(sys.modules, {'app.models.trade': MagicMock()})

    # Mock gspread.service_account to prevent actual Google Sheets API calls
    mock_gspread_client = MagicMock()
    mock_gspread_client.open.return_value.sheet1 = MagicMock()
    session_mocker.patch('gspread.service_account', return_value=mock_gspread_client)

    # Patch the TelegramService and GoogleSheetsService classes to return our mocks
    session_mocker.patch('app.services.telegram.TelegramService', return_value=mock_telegram_service)
    session_mocker.patch('app.services.google_sheets.GoogleSheetsService', return_value=mock_google_sheets_service)


@pytest.fixture
def sma_crossover_strategy(mock_alpaca_service, mock_telegram_service, mock_google_sheets_service):
    # Now import the modules that depend on config
    from app.strategies.sma_crossover import SmaCrossover

    strategy = SmaCrossover(
        alpaca_service=mock_alpaca_service,
        telegram_service=mock_telegram_service,
        google_sheets_service=mock_google_sheets_service,
        short_window=2,
        long_window=4,
        trade_percentage=0.1
    )
    return strategy

@pytest.mark.asyncio
async def test_sma_crossover_buy_signal(sma_crossover_strategy, mock_alpaca_service, mock_telegram_service, mock_google_sheets_service, mock_db_session):
    # Mock historical data for a buy signal
    # Ensure short_mavg crosses above long_mavg at the last point
    data = {
        'close': [10, 10, 10, 10, 10, 10, 10, 10, 20, 21],
    }
    mock_df = pd.DataFrame(data)
    mock_alpaca_service.api.get_bars.return_value.df = mock_df

    # Mock get_position to return 0 (no current position)
    sma_crossover_strategy.get_position = AsyncMock(return_value=0.0)

    # Mock submit_order
    mock_order = MagicMock()
    mock_order.qty = 1
    mock_order.filled_avg_price = 15.0
    mock_order.side = 'buy'
    mock_alpaca_service.submit_order.return_value = mock_order

    await sma_crossover_strategy.run("SPY", "1Min", mock_db_session)

    mock_alpaca_service.api.get_bars.assert_called_once()
    sma_crossover_strategy.get_position.assert_called_once_with("SPY")
    mock_telegram_service.send_message.assert_called_once_with("Buy signal for SPY")
    mock_alpaca_service.submit_order.assert_called_once()
    mock_google_sheets_service.export_trades.assert_called_once()

@pytest.mark.asyncio
async def test_sma_crossover_sell_signal(sma_crossover_strategy, mock_alpaca_service, mock_telegram_service, mock_google_sheets_service, mock_db_session):
    # Mock historical data for a sell signal
    # Ensure short_mavg crosses below long_mavg at the last point
    data = {
        'close': [21, 20, 10, 10, 10, 10, 10, 10, 10, 10],
    }
    mock_df = pd.DataFrame(data)
    mock_alpaca_service.api.get_bars.return_value.df = mock_df

    # Mock get_position to return a positive value (current position)
    sma_crossover_strategy.get_position = AsyncMock(return_value=1.0)

    # Mock submit_order
    mock_order = MagicMock()
    mock_order.qty = 1
    mock_order.filled_avg_price = 10.0
    mock_order.side = 'sell'
    mock_alpaca_service.submit_order.return_value = mock_order

    await sma_crossover_strategy.run("SPY", "1Min", mock_db_session)

    mock_alpaca_service.api.get_bars.assert_called_once()
    sma_crossover_strategy.get_position.assert_called_once_with("SPY")
    mock_telegram_service.send_message.assert_called_once_with("Sell signal for SPY")
    mock_alpaca_service.submit_order.assert_called_once()
    mock_google_sheets_service.export_trades.assert_called_once()

@pytest.mark.asyncio
async def test_sma_crossover_no_signal(sma_crossover_strategy, mock_alpaca_service, mock_telegram_service, mock_google_sheets_service, mock_db_session):
    # Mock historical data for no signal
    data = {
        'close': [10, 11, 10, 11, 10, 11, 10, 11, 10, 11],
    }
    mock_df = pd.DataFrame(data)
    mock_alpaca_service.api.get_bars.return_value.df = mock_df

    # Mock get_position to return 0 (no current position)
    sma_crossover_strategy.get_position = AsyncMock(return_value=0.0)

    await sma_crossover_strategy.run("SPY", "1Min", mock_db_session)

    mock_alpaca_service.api.get_bars.assert_called_once()
    sma_crossover_strategy.get_position.assert_called_once_with("SPY")
    mock_telegram_service.send_message.assert_not_called()
    mock_alpaca_service.submit_order.assert_not_called()
    mock_google_sheets_service.export_trades.assert_not_called()
