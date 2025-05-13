import pytest
from unittest.mock import patch
from f1_backend import get_driver_stat, AVAILABLE_STATS, ALLOWED_DRIVERS


@patch("f1_backend.fastf1.get_session")
def test_supported_driver_and_stat(mock_get_session):
    mock_session = mock_get_session.return_value
    mock_session.load.return_value = None

    mock_lap_data = {
        "LapNumber": [1, 2, 3],
        "LapTime": [10.0, 11.0, 12.0],
        "Compound": ["SOFT", "MEDIUM", "HARD"],
    }

    import pandas as pd
    mock_session.laps.pick_driver.return_value = pd.DataFrame(mock_lap_data)

    laps, data, title = get_driver_stat(2025, "Bahrain", "VER", "Lap Time")
    assert laps == [1, 2, 3]
    assert data == [10.0, 11.0, 12.0]
    assert "Verstappen" in title
