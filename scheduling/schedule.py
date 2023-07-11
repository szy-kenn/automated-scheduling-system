from .scheduled_course import ScheduledCourse

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

    def print(self):
        print(self.name)
        for key, val in self.schedule.items():
            print(key)
            scheduled_course : ScheduledCourse
            for scheduled_course in val:
                print(f"{scheduled_course.start_time} - {scheduled_course.end_time} | {scheduled_course.name}")

    def add_course(self, course: ScheduledCourse):
        self.schedule[course.day.capitalize()].append(course)

    def get_by_day(self, day: str):
        """Returns the schedule for a given day (str)"""
        return self.schedule[day]
    
    def __repr__(self) -> str:
        return self.name

