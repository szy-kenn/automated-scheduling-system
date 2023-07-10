from .course import Course

class ScheduledCourse(Course):

    def __init__(self, course: Course):
        super().__init__(*course.all_attr)

    def assign_sched(self, start_time: str, end_time: str, day: str):
        """
        Assign a timeframe for this Course
        """
        self.start_time = start_time
        self.end_time = end_time
        self.day = day