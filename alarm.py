from time import sleep
from time_clock import TimeClock
import clock_utils as clock

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
        done = False
        self._off = False
        while not done and not self._off:
            curr_hour, curr_min, curr_sec = clock.get_current_time()
            if curr_hour != self._time._hour:
                self._sleep_until_alarm_hour(curr_hour)
                continue
            if curr_min != self._time._minutes:
                self._sleep_until_alarm_minute(curr_min)
                continue
            if curr_sec != self._time._seconds:
                self._sleep_until_alarm_second(curr_sec)
                continue
            done = True
        self._alarm.warn()
    
    def _sleep_until_alarm_hour(self, curr_hour):
        to_be_elapsed = (self._time._hours-curr_hour)
        if to_be_elapsed < 0:
            to_be_elapsed = 23-to_be_elapsed
        sleep_for_h = clock.from_hours_to_secs(to_be_elapsed)
        sleep(sleep_for_h)
    
    def _sleep_until_alarm_minute(self, curr_min):
        to_be_elapsed = (self._time._minutes - curr_min)
        if to_be_elapsed < 0:
            sleep(clock.from_hours_to_secs(23)+clock.from_min_to_secs((-to_be_elapsed)-1))
            return
            
        if to_be_elapsed > 1:
            to_be_elapsed -= 1
            sleep_for_m = clock.from_min_to_secs(to_be_elapsed)
            sleep(sleep_for_m)
        
    def _sleep_until_alarm_second(self, curr_sec):
        to_be_elapsed = (self._time._seconds - curr_sec)
        if to_be_elapsed < 0:
            sleep(clock.from_min_to_secs(59)+59)
            return

        if to_be_elapsed > 1:
            sleep_for_s = to_be_elapsed-1
            sleep(sleep_for_s)