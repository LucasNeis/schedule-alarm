from time_clock import TimeClock
from schedule_handler import ScheduleHandler
import subprocess
from time import sleep
from threading import Thread
import clock_utils as clock

class Notifier:
    def notify(self, sender):
        if sender == "lunch break":
            self._waiting_loop("It's lunch break time!",
                "Stop for a quick lunch and rest. See you soon.",
                "Lunch break.")
            return
        if sender == "lunch return":
            self._waiting_loop("Time to get back!",
                "How was your lunch? Let's get back to work.",
                "Welcome back")
            return
        if sender == "leave":
            self._waiting_loop("Another day ends!",
                "Another days get to its end. Time to head out and get some rest, mate. See you next time. :)",
                "Good night")
            return
        return
    
    def update(self, alarm_type, sender):
        self.notify(alarm_type)
        sender.set_next(alarm_type)
        return
    
    def _waiting_loop(self, text_title, text_message, voice_message):
        t = Thread(target= self._message, args=[voice_message])
        self._aswered = False
        t.start()
        subprocess.run(["osascript", "-e", "display alert \""+ text_title + "\" message \"" + text_message + "\""])
        self._aswered = True
        
        t.join()
    
    def _message(self, voice_message):
        while not self._aswered:
            subprocess.run(["osascript", "-e", "say \"" + voice_message + "\""])
            sleep(2)
        

if __name__ == "__main__":
    # "osascript -e 'display notification \"hello world!\"\'"
    subprocess.run(["osascript", "-e", "display alert \"Welcome to work!\" message \"Another day begins. Lets start, shall we?\""])
    sh = ScheduleHandler(clock.now())
    sh.forecast(TimeClock(8, 48), TimeClock(1), TimeClock(13))
    notifier = Notifier()
    sh.subscribe(notifier.update)
    sh.run()
