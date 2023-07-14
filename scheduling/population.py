from .functions import *
from ._config import *
from .course import Course
from .scheduled_course import ScheduledCourse
from .schedule import Schedule
from .timeslot import Timeslot
from .timeslot_container import TimeslotContainer
import random
from copy import deepcopy

class Population:
    def __init__(self) -> None:
        self.population = []

    def print(self):
        for key, val in enumerate(self.population):
            print(key)
            for timeslot, sub in val.items():
                print(timeslot, sub)

    def initialize(self):
        individuals = [
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
        
        self.timeslots_week = [TimeslotContainer('Reference', time(hour=7, minute=30),
                            time(hour=21), 1.5) for i in range(6)]
        schedule = Schedule("Schedule")
        
        # while individuals: [X]
        #   choose an individual [X]
        #   invalid_day = True [X]
        #   while invalid_day: [X]
        #       choose another day [X]
        #       valid indices = get_valid_indices(day, course.type, (1.5hr, 3h)) [X]
        #       if len(valid indices) > 0: [X]
        #           invalid_day = False [X]
        #   chosen_timeslot = random choice in valid indices [X]
        #   if course is not techdoc: [X]
        #       chosen_timeslot_2 = chosen_day[get index of chosen_timeslot + 1] [X]
        #   assign the timeslots to the course
        #   pop the chosen timeslots in the chosen_day list
        
        added_individual = 0
        while added_individual != 11:
            # print("MAY LAMAN PA SA INDIVIDUALS")
            chosen_individual = individuals[random.randrange(len(individuals))] # RANDOM NA SUBJECT!
            
            invalid_day = True
            while invalid_day:
                chosen_day_idx = random.randrange(6)    # RANDOM NA ARAW! (0-5 / MON-SAT)
                chosen_day = self.timeslots_week[chosen_day_idx]
                valid_indices = self.get_valid_indices(chosen_day_idx, chosen_individual)

                if (len(valid_indices) > 0):
                    invalid_day = False

            chosen_timeslot_idx = random.choice(valid_indices)          
            chosen_individual.assign(Schedule.days[chosen_day_idx], chosen_day.container[chosen_timeslot_idx].start_time)
            schedule.add_course(chosen_individual)
            self.timeslots_week[chosen_day_idx].container.pop(chosen_timeslot_idx)

            if chosen_individual.code != "COMP20113":
                 self.timeslots_week[chosen_day_idx].container.pop(chosen_timeslot_idx)
            added_individual += 1

        self.population = schedule
    
    def get_valid_indices(self, chosen_day_idx, course) -> list:
        """Return a list of valid indices given the course and the chosen day index"""
        if course.code == 'COMP20113':
            if (len(self.timeslots_week[chosen_day_idx]) > 0):
                return deepcopy(self.timeslots_week[chosen_day_idx])
        
        valid_indices = []
        chosen_day = self.timeslots_week[chosen_day_idx]
        for idx, timeslot in enumerate(chosen_day.container):
            if idx < len(chosen_day.container) - 1:
                original_timeslot_idx = self.ref_timeslot_container.get_timeslot(timeslot.start_time)
                next_timeslot_idx_in_chosen_day = chosen_day.get_timeslot(self.ref_timeslot_container.container[original_timeslot_idx + 1].start_time) 
                if next_timeslot_idx_in_chosen_day != -1:
                    valid_indices.append(idx)
        return valid_indices