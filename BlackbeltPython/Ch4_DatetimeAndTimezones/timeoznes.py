#! /usr/bin/env python

from datetime import datetime, timedelta
import dateutil
from dateutil import tz
from dateutil import parser as dateparser

now = datetime.now()
print(now)

euwtz = tz.gettz('Europe/Warsaw')
euwtz = now.replace(tzinfo=euwtz)
print('After setting tzinfo:')
print(euwtz)
localtz = tz.gettz() # local timezone (according to os settings)
localnow = now.replace(tzinfo=localtz)

# dateutil offers a list of timezones:
zones = list(dateutil.zoneinfo.get_zonefile_instance().zones)
print(zones[:5])
len(zones)

# get info about the timezone
localtz = tz.gettz()
# Given a timestamp the timezone object can tell us what timezone it is
print(localtz)
print(localtz.tzname(now))


# Create a helper factory to generate timezone-aware timestamps
def utcnow():
    return datetime.now(tz=tz.tzutc())

now_utc = utcnow()
# When serializing the dates prefer ISO formats
iso_now = now_utc.isoformat()
print('iso-formatted timestamp:', iso_now)
# Such serialized date can then be parsed with dateutil.parser.isoparse
from_iso = dateparser.isoparse(iso_now)
print(from_iso)
