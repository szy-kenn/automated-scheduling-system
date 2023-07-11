from .scheduled_course import ScheduledCourse
from .timeslot import Timeslot
from .timeslot_container import TimeslotContainer
from datetime import time

class Schedule:
    def __init__(self, name, start_time: time = time(hour=7, minute=30), end_time : time = time(hour=21, minute=30)) -> None:
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.schedule = {
            'Monday': TimeslotContainer(self.start_time, self.end_time, 0.5),
            'Tuesday': TimeslotContainer(self.start_time, self.end_time, 0.5),
            'Wednesday': TimeslotContainer(self.start_time, self.end_time, 0.5),
            'Thursday': TimeslotContainer(self.start_time, self.end_time, 0.5),
            'Friday': TimeslotContainer(self.start_time, self.end_time, 0.5),
            'Saturday': TimeslotContainer(self.start_time, self.end_time, 0.5),
            'Sunday': TimeslotContainer(self.start_time, self.end_time, 0.5)
        }

    def print(self, day: str = None):
        """Print the Schedule, pass a 'day' argument to only print specific day in the Schedule"""
        if day != None:
            try:
                return self.schedule[day]
            except:
                raise ValueError(f"Unexpected value: {day} is not a valid argument.")
            
        print(self.name)
        for key, val in self.schedule.items():
            print(key)
            scheduled_course : ScheduledCourse
            for scheduled_course in val:
                print(f"{scheduled_course.start_time} - {scheduled_course.end_time} | {scheduled_course.name}")

    def add_course(self, course: ScheduledCourse):
        self.schedule[course.day.capitalize()].assign(course)
    
    def __repr__(self) -> str:
        return self.name

