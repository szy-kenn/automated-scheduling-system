from datetime import time, timedelta
from .schedule import Schedule
from .scheduled_course import ScheduledCourse
from math import floor, ceil

class Evaluator:

    def __init__(self, avg_dismissal: time, max_consecutive_classes: int) -> None:
        """
        Initialization for the Evaluator class
        
        
        """
        
        self.avg_dismissal = avg_dismissal
        self.avg_vacancy = None
        self.avg_classes = None
        self.avg_class_hrs = None
        self.max_consecutive_class_hrs = None
        self.vacancy_session_ratio = None
        self.max_consecutive_classes = max_consecutive_classes


    def evaluate(self, schedule: Schedule):
        dismissals = []
        for val in schedule.schedule.values():
            if (len(val) > 0):
                course: ScheduledCourse
                course = val[-1]
                # avg_dismissal = timedelta(hours=self.avg_dismissal.hour, minutes=self.avg_dismissal.minute)
                course_dismissal = timedelta(hours=course.end_time.hour, minutes=course.end_time.minute)
                dismissals.append(course_dismissal)

        avg = sum([dismissal.seconds for dismissal in dismissals])/3600 / 5
        course_avg_dismissal = timedelta(hours=floor(avg), minutes=(avg % floor(avg))*60)
        difference = timedelta(hours=self.avg_dismissal.hour, minutes=self.avg_dismissal.minute) - course_avg_dismissal
        print(difference)
                