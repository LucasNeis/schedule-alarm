from time_clock import TimeClock
from alarm import Alarm
import time_clock as clock

class ScheduleHandler:
    def __init__(self, entry):
        self._entry = entry
        self._subscript = []
        self._set = False
    
    def forecast(self, working_time, lunch_time, fixed_lunch_start=None):
        self._working_time = working_time
        self._remaning = working_time
        if fixed_lunch_start != None and type(fixed_lunch_start) is TimeClock:
            self._lunch_alarm = Alarm(fixed_lunch_start)
        else:
            self._lunch_alarm = Alarm(hours = self._entry + 4)
        fixed_lunch_start = self._lunch_alarm.get_alarm_time()
        
        self._return_alarm = Alarm(fixed_lunch_start.add(lunch_time))
        self._leave_alarm = Alarm(self._entry.add(working_time.add(lunch_time)))
        self._set = True
    
    def get_alarm_time(self, param: int) -> TimeClock:
        if param == 0:
            return self._lunch_alarm.get_alarm_time()
        if param == 1:
            return self._return_alarm.get_alarm_time()
        return self._leave_alarm.get_alarm_time()
    
    def run(self):
        if not self._set:
            raise "forecast not set"

        now = clock.now()
        if not now.in_the_future_of(self._lunch_alarm.get_alarm_time()):
            self._lunch_alarm.set_up_and_wait()
            self._notify_all("lunch break")

        now = clock.now()
        if not now.in_the_future_of(self._return_alarm.get_alarm_time()):
            self._return_alarm.set_up_and_wait()
            self._notify_all("lunch return")
        
        now = clock.now()
        if not now.in_the_future_of(self._leave_alarm.get_alarm_time()):
            self._leave_alarm.set_up_and_wait()
            self._notify_all("leave")
    
    def set_next(self, alarm_type):
        now = clock.now()
        if alarm_type == "lunch break":
            worked = now.subtract(self._entry)
            self._remaning = self._working_time.subtract(worked)
            self._return_alarm = Alarm(now.add(TimeClock(1)))
        elif alarm_type == "lunch return":
            self._leave_alarm = Alarm(now.add(self._remaning))
    
    def _notify_all(self, alarm_type):
        for subscriber in self._subscript:
            subscriber(alarm_type, self)
    
    def subscribe(self, subscriber):
        self._subscript.append(subscriber)
