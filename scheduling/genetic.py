from ._config import *
from .fitness import Fitness
from .scheduled_course import ScheduledCourse
from .population import Population
from .schedule import Schedule
from .timeslot_container import TimeslotContainer
import matplotlib.pyplot as plt
from datetime import time
from copy import deepcopy
from math import floor
import random

class Genetic:
    def __init__(self, population_size, growth_rate, mutation_rate, max_generations, avg_dismissal: time, avg_vacancy: int, avg_classes: int,
                 avg_class_hrs: int, max_consecutive_classes: int,  max_consecutive_class_hrs: int) -> None:
        
        self.evaluator = Fitness(avg_dismissal, avg_vacancy, avg_classes, 
                                   avg_class_hrs, max_consecutive_classes, max_consecutive_class_hrs)
        
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
        self.population = []
        self.population_size = population_size
        self.growth_rate = growth_rate
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations

        self.plots = []

    def start_world(self):
        self.initialize_generation()
        terminated = False
        for i in range(self.max_generations):
            self.calculate_fitness()
            self.selection()
        # self.evaluation()
        return 

    def initialize_generation(self):
        
        for i in range(self.population_size):
            self.timeslots_week = [TimeslotContainer('Reference', time(hour=7, minute=30),
                                time(hour=21), 1.5) for i in range(6)]
            schedule = Schedule("Schedule")
        
            added_individual = 0
            while added_individual != 11:
                # print("MAY LAMAN PA SA INDIVIDUALS")
                chosen_individual = self.individuals[random.randrange(len(self.individuals))] # RANDOM NA SUBJECT!
                
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

            self.population.append(schedule)
    
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

    def create_generation(self):
        pass

    def calculate_fitness(self):
        for idx, schedule in enumerate(self.population):
            schedule.calculate_fitness()

    def evaluation(self):
        pass

    def selection(self):
        self.mating_pool = []
        self.max_conflicts = max(schedule.conflicts for schedule in self.population)
        def get_mating_probability(conflicts):
            return 100 - (conflicts / (1 + self.max_conflicts) * 100)

        for schedule in self.population:
            # schedule.print()
            self.plots.append(schedule.conflicts)
            if schedule.conflicts == 0:
                print("ZERO")
                break
            # print(floor(get_mating_probability(schedule.conflicts)))
            for _ in range(floor(get_mating_probability(schedule.conflicts))):
                self.mating_pool.append(schedule)
            self.ranking()
            top2 = self.population[:2]  # ELITISM
        self.population = []
        self.population.extend(top2)
        while len(self.population) < self.population_size + (self.population_size * self.growth_rate):
            a_index = random.randrange(len(self.mating_pool))
            b_index = random.randrange(len(self.mating_pool))
            parent_a = (self.mating_pool[a_index])
            parent_b = (self.mating_pool[b_index])
            child = parent_a.crossover(parent_b)
            mutated_child = self.mutation(child)
            self.population.append(mutated_child)
            # print(len(self.new_generation))

    def ranking(self):
        copied_population = self.population
        sorted_conflicts = []
        for i in range(len(copied_population)):
            for j in range(len(copied_population)):
                if (copied_population[i].conflicts < copied_population[j].conflicts):
                    copied_population[i], copied_population[j] = copied_population[j], copied_population[i]

        # print([population.conflicts for population in copied_population])

    def crossover(self):
        """Uniform crossover"""
        pass
    
    def mutation(self, _schedule):
        schedule = deepcopy(_schedule)
        for idx, timeslot_container in enumerate(schedule.schedule):
            for idx2, timeslot in enumerate(timeslot_container.container):
                res = random.randint(0, self.mutation_rate * 10000)
                if res == 1:
                    new_scheduled_course_idx = random.randrange(len(self.individuals) + 1)
                    if new_scheduled_course_idx == len(self.individuals):
                        schedule.schedule[idx].container[idx2].assign(None)
                    else:
                        new_scheduled_course = self.individuals[new_scheduled_course_idx]
                        new_scheduled_course.assign(timeslot_container.name, timeslot.start_time)
                        schedule.schedule[idx].container[idx2].assign(new_scheduled_course)
                    # timeslot.assign(new_scheduled_course)
        return schedule
    
    def plot(self):
        pass