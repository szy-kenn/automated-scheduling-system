from .scheduled_course import ScheduledCourse
from .timeslot import Timeslot
class Schedule:
    def __init__(self, name) -> None:
        self.name = name
        self.schedule = {
            'Monday': [],
            'Tuesday': [],
            'Wednesday': [],
            'Thursday': [],
            'Friday': [],
            'Saturday': [],
            'Sunday': []
        }

    def generate_timeslot(self, size: int, repeat: int) -> list:
        timeslots = []
        for i in range(repeat):
            timeslots.append(Timeslot(size))

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
        self.schedule[course.day.capitalize()].append(course)
    
    def __repr__(self) -> str:
        return self.name

