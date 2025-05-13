import pytest
from unittest.mock import patch, MagicMock
from f1_backend import get_driver_stat


@patch("f1_backend.fastf1.get_session")
def test_supported_driver_and_stat(mock_get_session):
    mock_session = MagicMock()
    mock_get_session.return_value = mock_session

    mock_session.load.return_value = None

    import pandas as pd

    # Mock laps.pick_driver to return a DataFrame
    mock_laps = MagicMock()
    mock_laps.pick_driver.return_value = pd.DataFrame({
        "LapNumber": [1, 2, 3],
        "LapTime": pd.to_timedelta(["0:01:10", "0:01:11", "0:01:12"]),
        "Compound": ["SOFT", "MEDIUM", "HARD"]
    })

    # Inject mock_laps into mock_session
    mock_session.laps = mock_laps

    laps, data, title = get_driver_stat(2025, "Bahrain", "VER", "Lap Time")

    assert laps == [1, 2, 3]
    assert data == [70.0, 71.0, 72.0]
    assert "Verstappen" in title
