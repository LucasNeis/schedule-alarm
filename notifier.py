#!/usr/bin/python3

from os import error
from schedule_handler import ScheduleHandler
from time_clock import TimeClock
from time_clock import valid_time
from time_clock import _now
from threading import Thread
from time import sleep
import argparse
import subprocess
import notifier_message_generator as gen

class Notifier:
    def __init__(self,
                 voiceless = False,
                 verbose = False,
                 lunch_break_func  = lambda : "Lunch break.",
                 lunch_return_func = lambda : "Welcome back",
                 leave_func        = lambda : "Good night"):
        self._voiceless = voiceless
        self._verbose = verbose
        self._lunch_break_func  = lunch_break_func
        self._lunch_return_func = lunch_return_func
        self._leave_func        = leave_func

    def notify(self, sender):
        if self._verbose:
            print("Playing alarm for", sender, "now.")
        if sender == "lunch break":
            self._waiting_loop("It's lunch break time!",
                "Stop for a quick lunch and rest. See you soon.",
                self._lunch_break_func)
            return
        if sender == "lunch return":
            self._waiting_loop("Time to get back!",
                "How was your lunch? Let's get back to work.",
                self._lunch_return_func)
            return
        if sender == "leave":
            self._waiting_loop("Another day ends!",
                "Another day get to its end. Time to head out and get some rest, mate. See you next time. :)",
                self._leave_func)
            return
        return
    
    def update(self, alarm_type, sender):
        self.notify(alarm_type)
        sender.set_next(alarm_type)
        if self._verbose:
            now_ = _now()
            lunch = sh.get_alarm_time(0)
            ret = sh.get_alarm_time(1)
            leave = sh.get_alarm_time(2)
            print(now_, lunch, ret, leave)
            print("Some of your alarms have been rescheduled:\nLunch:", lunch, 
                "(done)" if now_.in_the_future_of(lunch) else "", "\nReturn:", ret,
                "(done)" if now_.in_the_future_of(ret) else "", "\nLeave:", leave)
        return
    
    def _waiting_loop(self, text_title, text_message, voice_message):
        t = Thread(target= self._message, args=[voice_message])
        self._aswered = False
        t.start()
        subprocess.run(["osascript", "-e", "display alert \""+ text_title + "\" message \"" + text_message + "\""])
        self._aswered = True
        
        t.join()
    
    def _message(self, voice_message):
        if self._voiceless:
            return
        while not self._aswered:
            subprocess.run(["osascript", "-e", "say \"" + voice_message() + "\""])
            sleep(2)

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-la", "--lunch", help="The time (H:M) you will be stopping for lunch. By default set to 13h.", type=valid_time)
    parser.add_argument("-lp", "--lunchperiod", help="The period of time (H:M) yout lunch break will take. By default set to 1 hour.", type=valid_time)
    parser.add_argument("-s", "--started", help="The time (H:M) you started your office day. By default set to now.", type=valid_time)
    parser.add_argument("-v", "--verbose", help="Increase output verbosity.", action="store_true")
    parser.add_argument("-vl", "--voiceless", help="Run without voice reminders.", action="store_true")
    parser.add_argument("-w", "--workinghours", help="The period of time you'll be working for. By default set to 8h48m.", type=valid_time)
    return parser.parse_args()

if __name__ == "__main__":
    args = arg_parse()
    _now = _now()
    starts = _now if args.started is None else args.started
    lunch = TimeClock(13) if args.lunch is None else args.lunch
    period = TimeClock(1) if args.lunchperiod is None else args.lunchperiod
    working_hours = TimeClock(8, 48) if args.workinghours is None else args.workinghours

    subprocess.run(["osascript", "-e", "display alert \"Welcome to work!\" message \"I've started running exactly at " +
     str(_now) + ". Worry not! I'll make sure to take care of your schedule.\""])
        
    sh = ScheduleHandler(starts)
    sh.forecast(working_hours, period, lunch)
    if args.verbose:
        print("Your alarm have been initially set as follows:\nLunch:", sh.get_alarm_time(0), "\nReturn:",
         sh.get_alarm_time(1), "\nLeave:", sh.get_alarm_time(2))
    notifier = Notifier(args.voiceless, args.verbose, gen.random_lunch_break_message, gen.random_lunch_return_message, gen.random_leave_time_message)
    sh.subscribe(notifier.update)
    sh.run()
