# test_f1_backend.py
import pytest
from f1_backend import get_driver_stat, ALLOWED_DRIVERS, AVAILABLE_STATS

def test_supported_driver_and_stat():
    laps, data, title = get_driver_stat(2025, "Bahrain", "VER", "Lap Time")
    assert isinstance(laps, list)
    assert isinstance(data, list)
    assert isinstance(title, str)
    assert len(laps) == len(data)

def test_unsupported_driver():
    laps, data, title = get_driver_stat(2025, "Bahrain", "HAM", "Lap Time")
    assert laps == []
    assert data == []
    assert "not supported" in title

def test_invalid_stat_type():
    laps, data, title = get_driver_stat(2025, "Bahrain", "VER", "Banana Time")
    assert laps == []
    assert data == []
    assert "Unsupported stat" in title

def test_stat_options():
    for stat in AVAILABLE_STATS:
        laps, data, title = get_driver_stat(2025, "Bahrain", "VER", stat)
        assert isinstance(laps, list)
        assert isinstance(data, list)
        assert isinstance(title, str)

@pytest.mark.parametrize("driver_code", ALLOWED_DRIVERS.keys())
def test_each_allowed_driver(driver_code):
    laps, data, title = get_driver_stat(2025, "Bahrain", driver_code, "Lap Time")
    assert isinstance(laps, list)
    assert isinstance(data, list)
    assert isinstance(title, str)
