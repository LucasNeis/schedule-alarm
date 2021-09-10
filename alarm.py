from time import sleep
from time_clock import TimeClock
import time_clock as clock

class AlarmTeller:
    def warn(self):
        print("ALARM!")

class Alarm:
    _time = TimeClock(0)
    def __init__(self, hours, minutes=0, seconds=0, teller=AlarmTeller()):
        self._time = TimeClock(hours, minutes, seconds)
        self._alarm = teller
        self._off = True
    
    def __init__(self, time, teller=AlarmTeller()):
        self._time = time
        self._alarm = teller
        self._off = True

    def set_teller(self, new_teller):
        self._alarm = new_teller
    
    def get_alarm_time(self):
        return self._time
    
    def turn_off(self):
        self._off = True

    def set_up_and_wait(self):
        self._sleep_until_alarm()
        self._alarm.warn()
    
    def _sleep_until_alarm(self):
        now = clock.now()
        to_be_elapsed = self._time.subtract(now)
        sleeping_for = to_be_elapsed.in_seconds()
        print("I'll be sleeping for", sleeping_for, "seconds. I'll be waking up in", to_be_elapsed, ", exactly at", now.add(to_be_elapsed), ".")
        sleep(sleeping_for)