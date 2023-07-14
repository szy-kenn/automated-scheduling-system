from .timeslot_container import TimeslotContainer
from .timeslot import Timeslot
from .scheduled_course import ScheduledCourse
from datetime import time
from copy import deepcopy

class LegoStacker:

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    def __init__(self) -> None:
        pass

    def create_brick(self):
        pass

    def initialize(self):
        self.baseplates = []
        for i in range(6):
            self.baseplates.append(self.create_baseplate(LegoStacker.days[i]))

    def create_baseplate(self, name, start_time: time = time(hour=7, minute=30), end_time : time = time(hour=21, minute=30)):
        return TimeslotContainer(name, start_time, end_time, 0.5)

    def place(self, courses: list):
        solutions = []

        def assign(course, timeslot_idx, baseplate_idx, baseplates):
            # print(baseplates[baseplate_idx].container[timeslot_idx].start_time)
            scheduled_course = ScheduledCourse(course, baseplates[baseplate_idx].name, baseplates[baseplate_idx].container[timeslot_idx].start_time)
            copied_baseplate = deepcopy(baseplates[baseplate_idx])
            copied_baseplate.assign(scheduled_course)
            baseplates[baseplate_idx] = copied_baseplate
            return baseplates

        def backtracking(course_idx, baseplates):
            if course_idx == len(courses) - 1:
                solutions.append(baseplates)
                return baseplates
            
            for i in range(len(baseplates)):
                for position in baseplates[i].get_valid_positions():
                    new_baseplates = assign(courses[course_idx], position, i, baseplates)
                    backtracking(course_idx+1, new_baseplates)

        backtracking(0, self.baseplates)
        return solutions

    def stack(self, scheduled_course, desired_timeslot, timeslot_container):
        for timeslot in timeslot_container.container:
            if (desired_timeslot.start_time.strftime("%H:%M:%S") == timeslot.start_time.strftime("%H:%M:%S")
                and timeslot.course == None):
                timeslot_container.assign(scheduled_course)



