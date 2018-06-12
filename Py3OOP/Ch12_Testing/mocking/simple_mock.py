from flight_status_tracker import FlightStatusTracker
from unittest.mock import Mock
import py.test
import pytest


@pytest.fixture
def tracker():
    return FlightStatusTracker()


def test_mock_method(tracker):
    tracker.redis.set = Mock()
    with py.test.raises(ValueError) as ex:
        tracker.change_status("AC101", "lost")
    assert ex.value.args[0] == 'LOST is not a valid status'
    assert tracker.redis.set.call_count == 0
