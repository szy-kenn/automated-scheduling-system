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

        self.conflict_names = []

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

    def print(self, day: str = None, *, show_idx=False):
        """Print the Schedule, pass a 'day' argument to only print specific day in the Schedule"""
        if day != None:
            try:
                return self.schedule[day]
            except:
                raise ValueError(f"Unexpected value: {day} is not a valid argument.")
            
        print(self.name)
        idx = 0
        for key, val in enumerate(self.schedule):
            print(Schedule.days[key])
            scheduled_course : ScheduledCourse
            for key2, _timeslot in enumerate(val.container):
                print(f"{idx} | {_timeslot.start_time} - {_timeslot.end_time} | {_timeslot.course} | {_timeslot.course.type if _timeslot.course != None else ''} | {_timeslot.course.day if _timeslot.course != None else '' }")
                idx += 1

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
        self.conflict_names = []
        # HARD CONSTRAINTS
        all_courses_week = []
        for timeslot_container in self.schedule:
            all_courses_week.extend(timeslot_container.get_all_courses())

        for individual in self.individuals:
            # if self.get_course(individual) == -1:
            #     self.conflict_names.append("kulang ng course")
            #     conflict += 15    
            count = all_courses_week.count((individual.code, individual.type))
            if count != 2:
                self.conflict_names.append("DUPLICATES")
                conflict += 20

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
                self.conflict_names.append("lunch break")
                conflict += 5

        # may free day ka ba?
        class_day_counter = 0
        # assigned_timeslots = 0
        for timeslot_container in self.schedule:
            if len(timeslot_container.assigned_courses) > 0:
                class_day_counter += 1
            # assigned_timeslots += len(timeslot_container.assigned_timeslots)

        # if assigned_timeslots != 20:
        #     self.conflict_names.append("not equal to 20 timeslots")
        #     conflict += 10 * abs(assigned_timeslots - 20)

        if class_day_counter == 6:
            self.conflict_names.append("walang free day")
            conflict += 2
        
        # ano oras uwian mo?
        for timeslot_container in self.schedule:
            if timeslot_container.assigned_timeslots:
                # last_timeslot = timeslot_container.assigned_timeslots[len(timeslot_container.assigned_timeslots)-1]
                last_timeslot = timeslot_container.container[timeslot_container.get_timeslot(time(hour=19, minute=30))].course
                if (last_timeslot != None):
                    self.conflict_names.append("may klase sa last timeslot")
                    conflict += 3
                    # LAB ba yan?
                    if last_timeslot.type == "PHED 10042":
                        self.conflict_names.append("pe gabi")
                        conflict += 2
        
        # maximum classes
        for timeslot_container in self.schedule:
            if len(timeslot_container.assigned_courses) > 3:
                self.conflict_names.append("+3 klase")
                conflict += 4

        # magkahiwalay ba lab subjects mo? may kasama ba syang iba?
        lab_sub_day = None
        for timeslot_container in self.schedule:
            for assigned_courses in timeslot_container.assigned_courses:
                if assigned_courses.type == 'LAB':
                    if assigned_courses.start_time.hour >= 18:
                        self.conflict_names.append("gabi lab")
                        conflict += 5
                    if lab_sub_day == None:
                        lab_sub_day = assigned_courses.day
                    else:
                        if lab_sub_day != assigned_courses.day:
                            self.conflict_names.append("lab di sabay")
                            conflict += 8
                            if len(self.get_by_day(lab_sub_day).assigned_courses) > 1:
                                self.conflict_names.append("may kasabay na iba lab1")
                                conflict += 2
                            if len(self.get_by_day(assigned_courses.day).assigned_courses) > 1:
                                self.conflict_names.append("may kasabay na iba lab2")
                                conflict += 2
                        else:
                            if len(self.get_by_day(lab_sub_day).assigned_courses) > 2:
                                self.conflict_names.append("may kasabay na iba magkasama lab")
                                conflict += 3
        self.conflicts = conflict
        # print(conflict)

    def crossover(self, schedule, mutation_rate):
        """one-point crossover"""

        length = len(self.schedule) * len(self.schedule[0].container)
        # midpoint = random.randrange(length)
        midpoint = random.randrange(6)
        child = Schedule('Schedule')
        # print("MIDPOINT: ", midpoint)
        i = 0
        for i in range(midpoint):
            child.schedule[i] = deepcopy(self.schedule[i])
            for timeslot in child.schedule[i].container:
                if timeslot.course != None:
                    timeslot.course.day = child.schedule[i].name
        for i in range(midpoint, 6):
            child.schedule[i] = deepcopy(schedule.schedule[i])
            for timeslot in child.schedule[i].container:
                if timeslot.course != None:
                    timeslot.course.day = child.schedule[i].name
            i += 1

        # print("================================================================")
        # child.print(show_idx=True)
        # print("================================================================")
        child = self.mutation(child, mutation_rate)
        return child

    def mutation(self, child, mutation_rate):
        #TODO: Needs optimization, algorithm is taking a lot of time here
        # schedule = deepcopy(_schedule)

        def _mutate(scheduled_course, space) -> tuple:
            # returns tuple of the mutated timeslot and size (1, 2)
            if space == 1:
                random_mutation = random.random()
                if random_mutation <= mutation_rate:
                    flip_coin = random.randint(0, 1)
                    if flip_coin == 0:
                        return (None, 1)
                    else:
                        scheduled_course = ScheduledCourse(COMP20113, 'DIVIDED')
                        return (scheduled_course, 1)
                else:
                    return (scheduled_course, space)

            elif space == 2:

                random_mutation = random.random()
                
                if random_mutation <= mutation_rate:
                    random_choice = random.random()
                    if random_choice <= 0.083:
                        return (None, 1)
                    else:
                        random_course = random.choice(self.individuals)
                        return (random_course, (2 if random_course.type != 'DIVIDED' else 1))
                else:
                    return (scheduled_course, space)

        for idx, timeslot_container in enumerate(child.schedule):
            
            timeslot_idx = 0
            
            while timeslot_idx < len(timeslot_container.container):

                random_mutation = random.random()

                # for timeslot_idx in range(len(timeslot_container.container)):
                current_timeslot = timeslot_container.container[timeslot_idx]

                if (current_timeslot.course == None or 
                    (current_timeslot.course != None 
                        and current_timeslot.course.type == 'DIVIDED')):
                    
                    if timeslot_idx < len(timeslot_container.container) - 1:
                        next_timeslot = timeslot_container.container[timeslot_idx + 1]

                        if next_timeslot.course == None:
                            mutated_timeslot = _mutate(current_timeslot.course, 2)

                            if mutated_timeslot[0] != None:
                                mutated_timeslot[0].assign(child.schedule[idx].name, child.schedule[idx].container[timeslot_idx].start_time)
                                child.schedule[idx].assign(mutated_timeslot[0])

                                if (mutated_timeslot[1] == 2):
                                    timeslot_idx += 1

                            else:
                                child.schedule[idx].container[timeslot_idx].assign(None)

                        else:
                            mutated_timeslot = _mutate(current_timeslot.course, 1)
                            if mutated_timeslot[0] != None:
                                mutated_timeslot[0].assign(child.schedule[idx].name, child.schedule[idx].container[timeslot_idx].start_time)
                                child.schedule[idx].assign(mutated_timeslot[0])
                            else:
                                child.schedule[idx].container[timeslot_idx].assign(None)

                    else:
                        mutated_timeslot = _mutate(current_timeslot.course, 1)
                        if mutated_timeslot[0] != None:
                            mutated_timeslot[0].assign(child.schedule[idx].name, child.schedule[idx].container[timeslot_idx].start_time)
                            child.schedule[idx].assign(mutated_timeslot[0])
                        else:
                            child.schedule[idx].container[timeslot_idx].assign(None)
                else:
                    mutated_timeslot = _mutate(current_timeslot.course, 2)

                    if mutated_timeslot[0] != None:
                        mutated_timeslot[0].assign(child.schedule[idx].name, child.schedule[idx].container[timeslot_idx].start_time)
                        # print(timeslot_idx, child.schedule[idx].container[timeslot_idx].course, mutated_timeslot[0], child.schedule[idx].container[timeslot_idx].start_time)
                        child.schedule[idx].assign(mutated_timeslot[0])

                        if (mutated_timeslot[1] == 2):
                            timeslot_idx += 1
                        else:
                            child.schedule[idx].container[timeslot_idx+1].assign(None)

                    else:
                        child.schedule[idx].container[timeslot_idx].assign(None)
                        child.schedule[idx].container[timeslot_idx+1].assign(None)

                timeslot_idx += 1
        # i = 0
        # while i < 54: 
        #     res = random.random()
        #     if res < mutation_rate:
        #         if (child.schedule[int(i//9)].container[i%9].course == None or
        #             child.schedule[int(i//9)].container[i%9].course.type == 'DIVIDED'):
        #             if i%9 < len(child.schedule[int(i//9)].container) - 1:
        #                 if child.schedule[int(i//9)].container[(i%9)+1].course != None:
        #                     res2 = random.random()
        #                     if res2 >= 0.5:
        #                         child.schedule[int(i//9)].container[i%9].assign(None)
        #                     else:
        #                         new_scheduled_course = self.individuals[2]
        #                         new_scheduled_course.assign(child.schedule[int(i//9)].name, child.schedule[int(i//9)].container[i%9].start_time)
        #                         child.schedule[int(i//9)].assign(new_scheduled_course)
        #                 else:
        #                     new_scheduled_course_idx = random.randrange(len(self.individuals))
        #                     new_scheduled_course = self.individuals[new_scheduled_course_idx]
        #                     new_scheduled_course.assign(child.schedule[int(i//9)].name, child.schedule[int(i//9)].container[i%9].start_time)
        #                     child.schedule[int(i//9)].assign(new_scheduled_course)
        #             else:
        #                 res2 = random.random()
        #                 if res2 >= 0.5:
        #                     child.schedule[int(i//9)].container[i%9].assign(None)
        #                 else:
        #                     new_scheduled_course = self.individuals[2]
        #                     new_scheduled_course.assign(child.schedule[int(i//9)].name, child.schedule[int(i//9)].container[i%9].start_time)
        #                     child.schedule[int(i//9)].assign(new_scheduled_course)
        #         else:
        #             if i%9 < len(child.schedule[int(i//9)].container) - 1:
        #                 new_scheduled_course_idx = random.randrange(len(self.individuals))
        #                 new_scheduled_course = self.individuals[new_scheduled_course_idx]
        #                 new_scheduled_course.assign(child.schedule[int(i//9)].name, child.schedule[int(i//9)].container[i%9].start_time)
        #                 child.schedule[int(i//9)].assign(new_scheduled_course)
        #                 if new_scheduled_course.type == "DIVIDED":
        #                     child.schedule[int(i//9)].container[(i%9)+1].assign(None)
        #     i += 1

        return child
        
    def __repr__(self) -> str:
        return self.name

