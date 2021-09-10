from datetime import datetime as dt
import time

class TimeClock:
    def __init__(self, hour, minute=0, second=0):
        if hour < 0 or hour > 23:
            raise "Hours must be between 0 and 23"
        self._hour = hour
        if minute < 0 or minute > 59:
            raise "Minutes must be between 0 and 59"
        self._min = minute
        if second < 0 or minute > 59:
            raise "Minutes must be between 0 and 59"
        self._sec = second
    
    def __repr__(self):
         return ""

    def __str__(self):
        hour = str(self._hour)
        minute = str(self._min)
        second = str(self._sec)
        hour = hour if len(hour) > 1 else "0" + hour
        minute = minute if len(minute) > 1 else "0" + minute
        second = second if len(second) > 1 else "0" + second
        return hour + ":" + minute + ":" + second
    
    def hour(self):
        return self._hour
    
    def minute(self):
        return self._min
    
    def second(self):
        return self._sec
    
    def subtract(self, other):
        hour = (self._hour - other._hour)
        minute = (self._min - other._min)
        second = (self._sec - other._sec)

        if second < 0:
            minute -= 1
            second += 60
        
        if minute < 0:
            hour -= 1
            minute += 60
        
        if hour < 0:
            hour += 24

        return TimeClock(hour%24, minute%60, second%60)
    
    def add(self, other):
        hour = (self._hour + other._hour)
        minute = (self._min + other._min)
        second = (self._sec + other._sec)

        while second >= 60:
            second -= 60
            minute += 1
        
        while minute >= 60:
            minute -= 60
            hour += 1
        
        return TimeClock(hour%24, minute, second)
    
    def in_seconds(self):
        return from_hours_to_secs(self._hour) + from_min_to_secs(self._min) + self._sec

    def in_the_future_of(self, other):
        if self._hour > other._hour:
            return True
        elif self._hour < other._hour:
            return False
        if self._min > other._min:
            return True
        elif self._min < other._min:
            return False
        if self._sec > other._sec:
            return True
        return False


def get_current_time():
    now = dt.now()
    return int(now.strftime("%H")), int(now.strftime("%M")), int(now.strftime("%S"))

def from_hours_to_secs(hours):
    return hours*3600

def from_min_to_secs(min):
    return min*60

def now():
    return TimeClock(*get_current_time())

def valid_time(string_time: str) -> TimeClock:
    try:
        res = time.strptime(string_time, "%H:%M")
        got = TimeClock(res.tm_hour, res.tm_min, res.tm_sec)
    except ValueError:
        return now()
    return got
