import pytest
from unittest.mock import AsyncMock, MagicMock, patch


from fastapi import HTTPException

@pytest.fixture
def mock_alpaca_api():
    mock_api = MagicMock()
    return mock_api

@pytest.fixture
def alpaca_service(mock_alpaca_api, monkeypatch):
    monkeypatch.setenv("ALPACA_API_KEY", "test_key")
    monkeypatch.setenv("ALPACA_SECRET_KEY", "test_secret")
    monkeypatch.setenv("ALPACA_BASE_URL", "https://test-api.alpaca.markets")
    from app.services.alpaca import AlpacaService
    service = AlpacaService()
    service.api = mock_alpaca_api
    yield service

@pytest.mark.asyncio
async def test_get_account_info_success(alpaca_service, mock_alpaca_api):
    mock_account = MagicMock()
    mock_account._raw = {"cash": "10000", "portfolio_value": "10000"}
    mock_alpaca_api.get_account.return_value = mock_account

    # Mock the broadcast_json method of the manager
    with patch('app.core.connection_manager.manager.broadcast_json', new_callable=AsyncMock) as mock_broadcast_json:
        account_info = await alpaca_service.get_account_info()

        mock_alpaca_api.get_account.assert_called_once()
        mock_broadcast_json.assert_called_once_with({"type": "account_update", "data": mock_account._raw})
        assert account_info == mock_account

@pytest.mark.asyncio
async def test_get_account_info_failure(alpaca_service, mock_alpaca_api):
    mock_alpaca_api.get_account.side_effect = Exception("API Error")

    # Mock the broadcast_json method of the manager
    with patch('app.core.connection_manager.manager.broadcast_json', new_callable=AsyncMock) as mock_broadcast_json:
        with pytest.raises(HTTPException) as exc_info:
            await alpaca_service.get_account_info()

        assert exc_info.value.status_code == 500
        assert "API Error" in exc_info.value.detail
        mock_alpaca_api.get_account.assert_called_once()
        mock_broadcast_json.assert_not_called()

def test_submit_order_success(alpaca_service, mock_alpaca_api):
    mock_order = MagicMock()
    mock_alpaca_api.submit_order.return_value = mock_order

    order = alpaca_service.submit_order(symbol="SPY", qty=10, side="buy", type="market", time_in_force="gtc")

    mock_alpaca_api.submit_order.assert_called_once_with(
        symbol="SPY",
        qty=10,
        side="buy",
        type="market",
        time_in_force="gtc"
    )
    assert order == mock_order

def test_submit_order_failure(alpaca_service, mock_alpaca_api):
    mock_alpaca_api.submit_order.side_effect = Exception("Order Error")

    with pytest.raises(HTTPException) as exc_info:
        alpaca_service.submit_order("SPY", 10, "buy", "market", "gtc")

    assert exc_info.value.status_code == 500
    assert "Order Error" in exc_info.value.detail
    mock_alpaca_api.submit_order.assert_called_once()
