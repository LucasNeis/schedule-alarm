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

        if hour < 0:
            second = 60 - second
            minute = 60 - second
            hour += 24
        
        if minute < 0:
            second = 60 - second
            minute += 60
        
        if second < 0:
            second += 60
            minute += 59
            hour += 23

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
