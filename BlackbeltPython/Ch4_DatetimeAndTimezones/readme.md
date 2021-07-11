# Timestamps and timezones

Timestamps instantiated by `datetime` are not are not timezone aware.
* datetime.now() - local timezone timestamp - not timezone-aware
* datetime.utcnow() - utc timezone timestamp - still not timezone-aware!

Create timezone-aware timestamps with `dateutil`
```python
from dateutil import tz
tz.gettz('Europe/Paris')    # appropriate timezone for the location
tz.gettz('GMT+1')           # appropriate timezone object
tz.gettz()                  # local timezone (os settings)
```
