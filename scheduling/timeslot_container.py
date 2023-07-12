from .functions import *
from .timeslot import Timeslot
from .time_range import TimeRange
from datetime import time

class TimeslotContainer(TimeRange):
    def __init__(self, name, start_time: time, end_time, timeslot_size: int) -> None:
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
        super().__init__(start_time, end_time)
        self.name = name
        self.timeslot_size = timeslot_size
        self.size = (time_to_sec(self.end_time) - time_to_sec(self.start_time)) / 3600
        self.timeslot_count = self.size / self.timeslot_size
        self.container = []

        _start = time_to_td(self.start_time)
        for i in range(int(self.timeslot_count)):
            self.container.append(Timeslot(td_to_time(_start), td_to_time(_start + timedelta(seconds=self.timeslot_size * 3600))))
            _start += timedelta(seconds=self.timeslot_size * 3600)

    @property
    def assigned_timeslots(self) -> int:
        """Returns the number of assigned timeslots in the container"""
        assigned_timeslots = []
        for val in self.container:
            if val.course != None:
                assigned_timeslots.append(val)
        return assigned_timeslots
    
    def print(self):
        for timeslot in self.container:
            print(timeslot)
    
    def get_timeslot(self, time: time) -> int:
        """Returns the index of the timeslot given the time"""
        i = 0
        while time.strftime("%H:%M:%S") != self.container[i].start_time.strftime("%H:%M:%S"):
            i += 1
        return i

    def assign(self, item):
        """Assigns a ScheduledCourse in the timeslot"""

        _current_timeslot_idx = self.get_timeslot(item.start_time)
        while (time_to_sec(self.container[_current_timeslot_idx].end_time) != time_to_sec(item.end_time)):
            self.container[_current_timeslot_idx].assign(item)
            _current_timeslot_idx += 1
        self.container[_current_timeslot_idx].assign(item)

    def __repr__(self) -> str:
        return self.name

