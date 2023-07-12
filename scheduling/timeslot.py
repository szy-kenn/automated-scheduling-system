from .scheduled_course import ScheduledCourse
from .time_range import TimeRange
class Timeslot(TimeRange):
    def __init__(self, start_time, end_time) -> None:
        """
        Initialization of Timeslot class
        A subclass of TimeRange class
        
        Parameters
        ----------
        time_range : TimeRange
            the time range that the Timeslot is assigned to
        """

        super().__init__(start_time, end_time)
        self.course = None

    def assign(self, item: ScheduledCourse):
        self.course = item

    def __repr__(self) -> str:
        return f"{self.start_time} - {self.end_time} : {self.course}"