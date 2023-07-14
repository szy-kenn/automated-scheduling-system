from .course import Course
from .time_range import TimeRange
from .functions import *
from datetime import time

class ScheduledCourse(Course, TimeRange):

    def __init__(self, course: Course, type: str):
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
        type : str
            the type of session (lab/lec)
        """

        Course.__init__(self, *course.all_attr)
        self.type = type

    def assign(self, day, start_time, end_time=None):
        if end_time == None:
            if self.type == 'LEC':
                end_time = sec_to_time(time_to_sec(start_time) + (self.lec_units * 3600))
            elif self.type == 'LAB':
                end_time = sec_to_time(time_to_sec(start_time) + (self.lab_units * 3600))
            elif self.type == 'DIVIDED':
                end_time = sec_to_time(time_to_sec(start_time) + (1.5 * 3600))
        
        TimeRange.__init__(self, start_time, end_time)
        self.day = day
        # self.timeslot_unit = (self.total_units * 60) / 30
        
