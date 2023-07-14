from .scheduled_course import ScheduledCourse
from .timeslot import Timeslot
from .timeslot_container import TimeslotContainer
from datetime import time

class Schedule:

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def __init__(self, name, start_time: time = time(hour=7, minute=30), end_time : time = time(hour=21)) -> None:
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.schedule = [TimeslotContainer(Schedule.days[i], self.start_time, self.end_time, 1.5) for i in range(6)]
    
    def print(self, day: str = None):
        """Print the Schedule, pass a 'day' argument to only print specific day in the Schedule"""
        if day != None:
            try:
                return self.schedule[day]
            except:
                raise ValueError(f"Unexpected value: {day} is not a valid argument.")
            
        print(self.name)
        for key, val in enumerate(self.schedule):
            print(Schedule.days[key])
            scheduled_course : ScheduledCourse
            for _timeslot in val.container:
                print(f"{_timeslot.start_time} - {_timeslot.end_time} | {_timeslot.course}")

    def add_course(self, course: ScheduledCourse):
        self.schedule[Schedule.days.index(course.day.capitalize())].assign(course)

    def change_timeslot(self, course: ScheduledCourse, desired_timeslot: Timeslot, day: int):
        for idx, timeslot_container in enumerate(self.schedule):
            if timeslot_container.name == day:
                for timeslot in timeslot_container.container:
                    if (desired_timeslot.start_time.strftime("%H:%M:%S") == timeslot.start_time.strftime("%H:%M:%S")
                        and timeslot.course == None):
                        course.start_time = desired_timeslot.start_time
                        course.end_time = time(hour=desired_timeslot.start_time.hour + int(course.get_size('hours')))
                        self.schedule[idx].assign(course)

    def __repr__(self) -> str:
        return self.name

