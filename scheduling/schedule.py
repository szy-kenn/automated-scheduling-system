from .scheduled_course import ScheduledCourse
from .timeslot import Timeslot
from .timeslot_container import TimeslotContainer
from datetime import time

class Schedule:

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def __init__(self, name, start_time: time = time(hour=7, minute=30), end_time : time = time(hour=21, minute=30)) -> None:
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.schedule = [TimeslotContainer(Schedule.days[i], self.start_time, self.end_time, 0.5) for i in range(7)]

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
        self.schedule[Schedule.days.index(course.day.capitalize())].assign(course)
    
    def __repr__(self) -> str:
        return self.name

