'''
The mock library offers a context manager that allows us to replace attributes
on existing libraries with mock objects. When the context manager exits, the
original attribute is automatically restored to not impact other test cases
'''
import datetime
from flight_status_tracker import FlightStatusTracker
from unittest.mock import Mock
from unittest.mock import patch


def test_patch(tracker):
    tracker.redis.set = Mock()
    fake_now = datetime.datetime(2015, 4, 1)
    with patch('datetime.datetime') as dt:
        dt.now.return_value = fake_now
        tracker.change_status("AC102", "on time")
    dt.now.assert_called_once_with()
    tracker.redis.set.assert_called_once_with(
        'flightno:AC102',
        '2015-04-01T00:00:00|ON TIME')
