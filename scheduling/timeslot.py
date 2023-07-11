from .scheduled_course import ScheduledCourse

class Timeslot:
    def __init__(self, size) -> None:
        self.size = size
        self.course = None

    def assign(self, item: ScheduledCourse):
        self.course = item