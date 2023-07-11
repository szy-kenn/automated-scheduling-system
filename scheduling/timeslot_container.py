from .functions import *
from .timeslot import Timeslot
from datetime import time

class TimeslotContainer:
    def __init__(self, start_time: time, end_time, timeslot_size: int) -> None:
        """
        initialization of TimeslotContainer
        
        Parameters
        ---------  
        start_time : time
            start time of the timeslot container
        end_time : time
            end time of the timeslot container
        timeslot_size : int
            the size of the timeslot (in hours)

        """
        self.start_time = start_time
        self.end_time = end_time
        self.timeslot_size = timeslot_size
        self.size = (time_to_sec(self.end_time) - time_to_sec(self.start_time)) / 3600
        self.timeslot_count = self.size / self.timeslot_size
        self.container = {}

        _start = time_to_td(self.start_time)
        for i in range(int(self.timeslot_count)):
            self.container[td_to_time(_start).strftime("%H:%M:%S")] = Timeslot(self.timeslot_size)
            _start += timedelta(seconds=self.timeslot_size * 3600)

    @property
    def assigned_timeslots(self) -> int:
        """Returns the number of assigned timeslots in the container"""
        assigned_timeslots = []
        for val in self.container.values():
            if val.course != None:
                assigned_timeslots.append(val)
        return assigned_timeslots

    def get_timeslot(self, time):
        pass

    def assign(self, item):
        """Assigns a ScheduledCourse in the timeslot"""
        _current_time = time_to_td(item.start_time)
        while _current_time != time_to_td(item.end_time):
            self.container[td_to_time(_current_time).strftime("%H:%M:%S")].assign(item)
            _current_time += timedelta(seconds=self.timeslot_size * 3600)