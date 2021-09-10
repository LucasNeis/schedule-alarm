from random import randint
from file_reader import FileReader

_last = [-1, -1, -1]
reader = FileReader()
 
def _random_element_from_list(list, last_chosen):
    last = len(list)-1
    index = randint(0, last)
    while index == _last[last_chosen]:
        index = randint(0, last)
    _last[last_chosen] = index
    return list[index]

def random_lunch_break_message():
    _lunch_break = reader.read_into_list("./resources/lunch_break_speech.txt", True)
    return _random_element_from_list(_lunch_break, 0)

def random_lunch_return_message():
    _return_lunch = reader.read_into_list("./resources/lunch_return_speech.txt", True)
    return _random_element_from_list(_return_lunch, 1)

def random_leave_time_message():
    _leave_time = reader.read_into_list("./resources/leave_time_speech.txt", True)
    return _random_element_from_list(_leave_time, 2)