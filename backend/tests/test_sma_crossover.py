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
def mock_config_and_models(
    session_mocker: MockerFixture, mock_telegram_service, mock_google_sheets_service
):
    mock_config = MagicMock()
    mock_config.settings.ALPACA_API_KEY = "test_key"
    mock_config.settings.ALPACA_SECRET_KEY = "test_secret"
    mock_config.settings.ALPACA_BASE_URL = "https://test-api.alpaca.markets"
    mock_config.settings.TELEGRAM_BOT_TOKEN = "test_token"
    mock_config.settings.TELEGRAM_CHAT_ID = "test_chat_id"
    mock_config.settings.GOOGLE_SHEETS_CREDENTIALS = "{}"

    session_mocker.patch.dict(sys.modules, {"config": mock_config})

    session_mocker.patch.dict(sys.modules, {"app.models.trade": MagicMock()})

    mock_gspread_client = MagicMock()
    mock_gspread_client.open.return_value.sheet1 = MagicMock()
    session_mocker.patch("gspread.service_account", return_value=mock_gspread_client)

    session_mocker.patch(
        "app.services.telegram.TelegramService", return_value=mock_telegram_service
    )
    session_mocker.patch(
        "app.services.google_sheets.GoogleSheetsService",
        return_value=mock_google_sheets_service,
    )


@pytest.fixture
def sma_crossover_strategy(
    mock_alpaca_service, mock_telegram_service, mock_google_sheets_service
):
    from app.strategies.sma_crossover import SmaCrossover

    strategy = SmaCrossover(
        alpaca_service=mock_alpaca_service,
        telegram_service=mock_telegram_service,
        google_sheets_service=mock_google_sheets_service,
        short_window=2,
        long_window=4,
        trade_percentage=0.1,
    )
    return strategy


@pytest.mark.asyncio
async def test_sma_crossover_buy_signal(
    sma_crossover_strategy,
    mock_alpaca_service,
    mock_telegram_service,
    mock_google_sheets_service,
    mock_db_session,
):
    data = {
        "close": [
            10,
            10,
            10,
            10,
            10,
            10,
            10,
            10,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
        ],
    }
    mock_df = pd.DataFrame(data)
    mock_alpaca_service.get_bars.return_value.df = mock_df

    sma_crossover_strategy.get_position = AsyncMock(return_value=0.0)

    mock_order = MagicMock()
    mock_order.qty = 1
    mock_order.filled_avg_price = 15.0
    mock_order.side = "buy"
    mock_alpaca_service.submit_order.return_value = mock_order

    await sma_crossover_strategy.run("SPY", "1Min", mock_db_session)

    mock_alpaca_service.get_bars.assert_called_once()
    sma_crossover_strategy.get_position.assert_called_once_with("SPY")
    mock_telegram_service.send_message.assert_called_once()
    mock_alpaca_service.submit_order.assert_called_once()
    mock_google_sheets_service.export_trades.assert_called_once()


@pytest.mark.asyncio
async def test_sma_crossover_sell_signal(
    sma_crossover_strategy,
    mock_alpaca_service,
    mock_telegram_service,
    mock_google_sheets_service,
    mock_db_session,
):
    data = {
        "close": [21, 20, 10, 10, 10, 10, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    }
    mock_df = pd.DataFrame(data)
    mock_alpaca_service.get_bars.return_value.df = mock_df

    sma_crossover_strategy.get_position = AsyncMock(return_value=1.0)

    mock_order = MagicMock()
    mock_order.qty = 1
    mock_order.filled_avg_price = 10.0
    mock_order.side = "sell"
    mock_alpaca_service.submit_order.return_value = mock_order

    await sma_crossover_strategy.run("SPY", "1Min", mock_db_session)

    mock_alpaca_service.get_bars.assert_called_once()
    sma_crossover_strategy.get_position.assert_called_once_with("SPY")
    mock_telegram_service.send_message.assert_called_once()
    mock_alpaca_service.submit_order.assert_called_once()
    mock_google_sheets_service.export_trades.assert_called_once()


@pytest.mark.asyncio
async def test_sma_crossover_no_signal(
    sma_crossover_strategy,
    mock_alpaca_service,
    mock_telegram_service,
    mock_google_sheets_service,
    mock_db_session,
):
    data = {
        "close": [
            10,
            11,
            10,
            11,
            10,
            11,
            10,
            11,
            10,
            11,
            10,
            11,
            10,
            11,
            10,
            11,
            10,
            11,
            10,
            11,
        ],
    }
    mock_df = pd.DataFrame(data)
    mock_alpaca_service.get_bars.return_value.df = mock_df

    sma_crossover_strategy.get_position = AsyncMock(return_value=0.0)

    await sma_crossover_strategy.run("SPY", "1Min", mock_db_session)

    mock_alpaca_service.get_bars.assert_called_once()
    sma_crossover_strategy.get_position.assert_called_once_with("SPY")
    mock_telegram_service.send_message.assert_not_called()
    mock_alpaca_service.submit_order.assert_not_called()
    mock_google_sheets_service.export_trades.assert_not_called()
