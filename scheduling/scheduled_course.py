from .course import Course
from datetime import time

class ScheduledCourse(Course):

    def __init__(self, course: Course, day: str, start_time: time, end_time: time):
        """
        Creates an object reprensenting a ScheduledCourse, 
        a Course object that stores the schedule of its sessions.
        ScheduledCourse inherits from the class Course.

        Parameters
        ----------
        course : Course
            a Course object
        day : str
            the day the course session is scheduled
        start_time : time
            the start time of the session
        end_time : time
            the end time of the session
            
        """
        super().__init__(*course.all_attr)
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        
