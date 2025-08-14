import pytest
from unittest.mock import MagicMock, patch
import pandas as pd

# Assuming a DataService class will be created in app/services/data.py
# For now, we'll mock it or create a dummy class for testing purposes.

class MockDataService:
    def __init__(self, api_mock):
        self.api = api_mock

    def get_bars(self, symbol, timeframe, limit):
        # This would typically call self.api.get_bars
        pass

@pytest.fixture
def mock_alpaca_api():
    mock_api = MagicMock()
    return mock_api

@pytest.fixture
def data_service(mock_alpaca_api):
    # In a real scenario, you'd instantiate your actual DataService here
    # For now, we use a mock or dummy class
    service = MockDataService(mock_alpaca_api)
    return service

def test_get_bars_success(data_service, mock_alpaca_api):
    # Create a dummy DataFrame for the mock return value
    mock_df = pd.DataFrame({
        'open': [100, 101],
        'high': [102, 103],
        'low': [99, 100],
        'close': [101, 102],
        'volume': [1000, 1100]
    })
    mock_alpaca_api.get_bars.return_value.df = mock_df

    # Assuming DataService.get_bars calls alpaca_api.get_bars
    # For this test, we'll directly call the mocked api method
    bars = mock_alpaca_api.get_bars("SPY", "1Min", limit=2).df

    mock_alpaca_api.get_bars.assert_called_once_with("SPY", "1Min", limit=2)
    pd.testing.assert_frame_equal(bars, mock_df)

def test_get_bars_failure(data_service, mock_alpaca_api):
    mock_alpaca_api.get_bars.side_effect = Exception("Data fetch error")

    with pytest.raises(Exception, match="Data fetch error"):
        mock_alpaca_api.get_bars("SPY", "1Min", limit=2)

    mock_alpaca_api.get_bars.assert_called_once()
