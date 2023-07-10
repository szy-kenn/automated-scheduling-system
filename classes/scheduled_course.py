from .course import Course
from datetime import time

class ScheduledCourse(Course):

    def __init__(self, course: Course, day: str, start_time: time, end_time: time):
        """
        Creates an object reprensenting a ScheduledCourse
        ScheduledCourse inherits from the class Course

        Parameters
        ----------
        course : Course
            a Course object 
        """
        super().__init__(*course.all_attr)
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        
