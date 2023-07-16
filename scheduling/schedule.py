from ._config import *
from .scheduled_course import ScheduledCourse
from .timeslot import Timeslot
from .timeslot_container import TimeslotContainer
from datetime import time
from copy import deepcopy
import random
class Schedule:

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def __init__(self, name, start_time: time = time(hour=7, minute=30), end_time : time = time(hour=21)) -> None:
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.schedule = [TimeslotContainer(Schedule.days[i], self.start_time, self.end_time, 1.5) for i in range(6)]
        self.conflicts = 0

        self.individuals = [
                ScheduledCourse(COMP20093, "LAB"),
                ScheduledCourse(COMP20103, "LAB"),
                ScheduledCourse(COMP20113, "DIVIDED"),
                ScheduledCourse(COSC30033, "LEC"),
                ScheduledCourse(COSCFE2, "LEC"),
                ScheduledCourse(PHED10042, "LEC"),
                ScheduledCourse(GEED10073, "LEC"),
                ScheduledCourse(GEED20113, "LEC"),
                ScheduledCourse(COMP20093, "LEC"),
                ScheduledCourse(COMP20103, "LEC"),
                ScheduledCourse(COMP20113, "DIVIDED")]
    
        self.ref_timeslot_container = TimeslotContainer('Reference', time(hour=7, minute=30),
                                                    time(hour=21), 1.5)
    def get_by_day(self, day) -> list:
        return self.schedule[Schedule.days.index(day)]

    def get_course(self, course) -> tuple:
        """Returns the tuple of indices of timeslot and timeslot container in the schedule"""
        for idx, time_container in enumerate(self.schedule):
            for idx2, timeslot in enumerate(time_container.container):
                if timeslot.course != None:
                    if timeslot.course.code == course.code and timeslot.course.type == course.type:
                        return (idx, idx2)                 
        return -1

    def print(self, day: str = None):
        """Print the Schedule, pass a 'day' argument to only print specific day in the Schedule"""
        if day != None:
            try:
                return self.schedule[day]
            except:
                raise ValueError(f"Unexpected value: {day} is not a valid argument.")
            
        print(self.name)
        for key, val in enumerate(self.schedule):
            print(Schedule.days[key])
            scheduled_course : ScheduledCourse
            for _timeslot in val.container:
                print(f"{_timeslot.start_time} - {_timeslot.end_time} | {_timeslot.course} | {_timeslot.course.type if _timeslot.course != None else ''}")

    def add_course(self, course: ScheduledCourse):
        self.schedule[Schedule.days.index(course.day.capitalize())].assign(course)

    def change_timeslot(self, course: ScheduledCourse, desired_timeslot: Timeslot, day: int):
        for idx, timeslot_container in enumerate(self.schedule):
            if timeslot_container.name == day:
                for timeslot in timeslot_container.container:
                    if (desired_timeslot.start_time.strftime("%H:%M:%S") == timeslot.start_time.strftime("%H:%M:%S")
                        and timeslot.course == None):
                        course.start_time = desired_timeslot.start_time
                        course.end_time = time(hour=desired_timeslot.start_time.hour + int(course.get_size('hours')))
                        self.schedule[idx].assign(course)

    def calculate_fitness(self):
        conflict = 0
        # HARD CONSTRAINTS
        for individual in self.individuals:
            if self.get_course(individual) == -1:
                conflict += 15

        # for timeslot_container in self.schedule:
        #     for idx, timeslot in enumerate(timeslot_container.container):
        #         if timeslot.course != None:
        #             if timeslot.course.type != "DIVIDED":
        #                 if idx < len(timeslot_container.container) - 1:
        #                     if timeslot_container.container[idx+1].course != None:
        #                         if timeslot_container.container[idx+1].course.code != timeslot.course.code:
        #                             conflict += 10
        #                     else:
        #                         conflict += 10
        #                 else:
        #                     conflict += 10

        # may lunch break ka ba?
        for timeslot_container in self.schedule:
            if (timeslot_container.container[timeslot_container.get_timeslot(time(hour=10, minute=30))].course != None
                and timeslot_container.container[timeslot_container.get_timeslot(time(hour=12))].course != None):
                conflict += 1

        # may free day ka ba?
        class_day_counter = 0
        assigned_timeslots = 0
        for timeslot_container in self.schedule:
            if len(timeslot_container.assigned_courses) > 0:
                class_day_counter += 1
            assigned_timeslots += len(timeslot_container.assigned_timeslots)

        if assigned_timeslots != 20:
            conflict += 10

        if class_day_counter == 6:
            conflict += 1
        
        # ano oras uwian mo?
        for timeslot_container in self.schedule:
            if timeslot_container.assigned_timeslots:
                # last_timeslot = timeslot_container.assigned_timeslots[len(timeslot_container.assigned_timeslots)-1]
                last_timeslot = timeslot_container.container[timeslot_container.get_timeslot(time(hour=19, minute=30))].course
                if (last_timeslot != None):
                    conflict += 1
                    # LAB ba yan?
                    if last_timeslot.type == "PHED 10042":
                        conflict += 2
        
        # maximum classes
        for timeslot_container in self.schedule:
            if len(timeslot_container.assigned_courses) > 3:
                conflict += 1

        # magkahiwalay ba lab subjects mo? may kasama ba syang iba?
        lab_sub_day = None
        for timeslot_container in self.schedule:
            for assigned_courses in timeslot_container.assigned_courses:
                if assigned_courses.type == 'LAB':
                    if assigned_courses.start_time.hour >= 18:
                        conflict += 2
                    if lab_sub_day == None:
                        lab_sub_day = assigned_courses.day
                    else:
                        if lab_sub_day != assigned_courses.day:
                            conflict += 5
                            if len(self.get_by_day(lab_sub_day).assigned_courses) > 1:
                                conflict += 1
                            if len(self.get_by_day(assigned_courses.day).assigned_courses) > 1:
                                conflict += 1
                        else:
                            if len(self.get_by_day(lab_sub_day).assigned_courses) > 2:
                                conflict += 2
        self.conflicts = conflict
        # print(conflict)

    def crossover(self, schedule, mutation_rate):
        """one-point crossover"""

        length = len(self.schedule) * len(self.schedule[0].container)
        midpoint = random.randrange(length)
        child = Schedule('Schedule')

        i = 0
        while i < length:
            two_timeslots = False
            if i < midpoint:
                course = self.schedule[int(i//9)].container[i%9].course
                if course != None:
                    if course.type != "DIVIDED":
                        if i < midpoint - 1:
                            i += 1
                            next_course = self.schedule[int(i//9)].container[i%9].course
                            if next_course != None and next_course.code == course.code and next_course.type == course.type:
                                child.schedule[int((i-1)//9)].assign(course)
                                # child.schedule[int(i//9)].container[i%9].assign(course)
                                two_timeslots = True
                                child = self.mutation(child, int((i-1)//9), (i-1)%9, mutation_rate)
                                continue
                            else:
                                continue
                    else:
                        child.schedule[int(i//9)].container[i%9].assign(course)
                else:
                    child.schedule[int(i//9)].container[i%9].assign(course)
            else:
                course = schedule.schedule[int(i//9)].container[i%9].course
                if course != None:
                    if course.type != "DIVIDED":
                        if i < length - 1 and i > midpoint:
                            i += 1
                            next_course = schedule.schedule[int(i//9)].container[i%9].course
                            if next_course != None and next_course.code == course.code and next_course.type == course.type:
                                child.schedule[int((i-1)//9)].assign(course)
                                # child.schedule[int(i//9)].container[i%9].assign(course)
                                two_timeslots = True
                                child = self.mutation(child, int((i-1)//9), (i-1)%9, mutation_rate)
                                continue
                            else:
                                continue
                    else:
                        child.schedule[int(i//9)].assign(course)
                else:
                    child.schedule[int(i//9)].container[i%9].assign(course)
        # for i in range(length):
        #     if i < midpoint:
        #         child.schedule[int(i//9)].container[i%9].assign(self.schedule[int(i//9)].container[i%9].course)
        #     else:
        #         child.schedule[int(i//9)].container[i%9].assign(schedule.schedule[int(i//9)].container[i%9].course)
            # child = self.mutation(child, int(i//9), i%9, mutation_rate)
            # if two_timeslots:
            #     child = self.mutation(child, int(i//9), i%9, mutation_rate, )
            # else:
            child = self.mutation(child, int(i//9), i%9, mutation_rate)
            i += 1
 
        return child
    
    def mutation(self, child, idx1, idx2, mutation_rate):
        #TODO: Needs optimization, algorithm is taking a lot of time here
        # schedule = deepcopy(_schedule)
        res = random.random()
        if res < mutation_rate:
            if (child.schedule[idx1].container[idx2].course == None or
                child.schedule[idx1].container[idx2].course.type == 'DIVIDED'):
                if idx2 < len(child.schedule[idx1].container) - 1:
                    if child.schedule[idx1].container[idx2+1].course != None:
                        res2 = random.random()
                        if res2 >= 0.5:
                            child.schedule[idx1].container[idx2].assign(None)
                        else:
                            new_scheduled_course = self.individuals[2]
                            new_scheduled_course.assign(child.schedule[idx1].name, child.schedule[idx1].container[idx2].start_time)
                            child.schedule[idx1].assign(new_scheduled_course)
                    else:
                        new_scheduled_course_idx = random.randrange(len(self.individuals))
                        new_scheduled_course = self.individuals[new_scheduled_course_idx]
                        new_scheduled_course.assign(child.schedule[idx1].name, child.schedule[idx1].container[idx2].start_time)
                        child.schedule[idx1].assign(new_scheduled_course)
                else:
                    res2 = random.random()
                    if res2 >= 0.5:
                        child.schedule[idx1].container[idx2].assign(None)
                    else:
                        new_scheduled_course = self.individuals[2]
                        new_scheduled_course.assign(child.schedule[idx1].name, child.schedule[idx1].container[idx2].start_time)
                        child.schedule[idx1].assign(new_scheduled_course)
            else:
                if idx2 < len(child.schedule[idx1].container) - 1:
                    new_scheduled_course_idx = random.randrange(len(self.individuals))
                    new_scheduled_course = self.individuals[new_scheduled_course_idx]
                    new_scheduled_course.assign(child.schedule[idx1].name, child.schedule[idx1].container[idx2].start_time)
                    child.schedule[idx1].assign(new_scheduled_course)
                    if new_scheduled_course.type == "DIVIDED":
                        child.schedule[idx1].container[idx2+1].assign(None)

            # new_scheduled_course_idx = random.randrange(len(self.individuals))
            # if new_scheduled_course_idx == len(self.individuals):
            #     child.schedule[idx1].container[idx2].assign(None)
            # else:
            # new_scheduled_course = self.individuals[new_scheduled_course_idx]
            # new_scheduled_course.assign(child.schedule[idx1].name, child.schedule[idx1].container[idx2].start_time)
            # child.schedule[idx1].container[idx2].assign(new_scheduled_course)
        return child
        
    def __repr__(self) -> str:
        return self.name

