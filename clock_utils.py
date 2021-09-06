from datetime import datetime as dt
from time_clock import TimeClock

def get_current_time():
    now = dt.now()
    return int(now.strftime("%H")), int(now.strftime("%M")), int(now.strftime("%S"))

def from_hours_to_secs(hours):
    return hours*3600

def from_min_to_secs(min):
    return min*60

def now():
    return TimeClock(*get_current_time())