import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock, AsyncMock
import sys


@pytest.fixture(scope="session")
def session_mocker(pytestconfig):
    """Session-scoped mocker fixture."""
    return MockerFixture(pytestconfig)


@pytest.fixture(scope="session", autouse=True)
def mock_all_services_and_config(session_mocker: MockerFixture):
    # Create explicit mocks for services
    mock_telegram_service_instance = MagicMock()
    mock_telegram_service_instance.send_message = AsyncMock()

    mock_google_sheets_service_instance = MagicMock()
    mock_google_sheets_service_instance.export_trades = MagicMock()

    # Create a mock for the config module and its settings
    mock_config_module = MagicMock()
    mock_config_module.settings.ALPACA_API_KEY = "test_key"
    mock_config_module.settings.ALPACA_SECRET_KEY = "test_secret"
    mock_config_module.settings.ALPACA_BASE_URL = "https://test-api.alpaca.markets"
    mock_config_module.settings.TELEGRAM_BOT_TOKEN = "test_token"
    mock_config_module.settings.TELEGRAM_CHAT_ID = "test_chat_id"
    mock_config_module.settings.GOOGLE_SHEETS_CREDENTIALS = "{}"

    # Patch sys.modules to return our mock objects when modules are imported
    session_mocker.patch.dict(
        sys.modules,
        {
            "config": mock_config_module,
            "app.services.telegram": MagicMock(
                TelegramService=MagicMock(return_value=mock_telegram_service_instance)
            ),
            "app.services.google_sheets": MagicMock(
                GoogleSheetsService=MagicMock(
                    return_value=mock_google_sheets_service_instance
                )
            ),
            "app.models.trade": MagicMock(),  # To prevent SQLAlchemy re-registration
        },
    )

    # Yield control to tests, then clean up if necessary (though mocker handles most of it)
    yield

    # Clean up sys.modules if necessary (mocker.patch.dict handles this on teardown)


@pytest.fixture
def mock_alpaca_service():
    service = MagicMock()
    service.api = MagicMock()
    service.get_account_info = AsyncMock(return_value=MagicMock(buying_power="10000"))
    return service


@pytest.fixture
def mock_telegram_service_instance(mock_all_services_and_config):
    # This fixture now just returns the mocked instance created in mock_all_services_and_config
    # We need to re-import the service to get the patched version
    from app.services.telegram import TelegramService

    return TelegramService()


@pytest.fixture
def mock_google_sheets_service_instance(mock_all_services_and_config):
    from app.services.google_sheets import GoogleSheetsService

    return GoogleSheetsService()


@pytest.fixture
def mock_db_session():
    db = MagicMock()
    return db
