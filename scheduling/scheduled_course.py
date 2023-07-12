from .course import Course
from .time_range import TimeRange
from datetime import time

class ScheduledCourse(Course, TimeRange):

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
        print(*course.all_attr)
        Course.__init__(self, *course.all_attr)
        TimeRange.__init__(self, start_time, end_time)
        self.day = day
        self.timeslot_unit = (self.total_units * 60) / 30
        
