from ._config import *
from .fitness import Fitness
from .scheduled_course import ScheduledCourse
from .population import Population
from .schedule import Schedule
from .timeslot_container import TimeslotContainer
import matplotlib.pyplot as plt
from datetime import time, datetime
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
        self.mutation_count_list = []
        self.mutation_count = 0
        self.current_generation = 0

    def start_world(self):
        print("Starting world ", datetime.now().time())
        self.initialize_generation()
        terminated = False
        for i in range(self.max_generations):
            self.calculate_fitness()
            res = self.selection()
            if res:
                break
        self.evaluation()
        self.plot()
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
            # schedule.print()
        self.current_generation += 1
        
        print("Finish initializing world ", datetime.now().time())

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
        print("Calculating fitness ", datetime.now().time())
        for idx, schedule in enumerate(self.population):
            schedule.calculate_fitness()

    def evaluation(self):
        # self.ranking()
        self.calculate_fitness()
        idx = min(sched.conflicts for sched in self.population)
        for sched in self.population:
            if sched.conflicts == idx:
                print(sched.conflicts)
                print(sched.conflict_names)
                sched.print()
                break
        # print(f"BEST SCHEDULE : (conflicts = {self.population[0].conflicts})")
        # self.population[0].print()

    def selection(self):
        print("Starting selection process ", datetime.now().time())
        self.mating_pool = []
        self.max_conflicts = max(schedule.conflicts for schedule in self.population)
        
        def get_mating_probability(conflicts):
            # return 10
            return 100 - (conflicts / (1 + self.max_conflicts) * 100)

        
        self.plots.append(sum(sched.conflicts for sched in self.population) / len(self.population))
        for schedule in self.population:
            # schedule.print()
            print(schedule.conflicts)

            if schedule.conflicts <= 2:
                print(schedule.conflicts)
                print(schedule.conflict_names)
                schedule.print()
                return True
            
            for _ in range(floor(get_mating_probability(schedule.conflicts))):
                self.mating_pool.append(schedule)

            # if len(self.mating_pool) == 0:
            #     return True
        print("Start ranking the mating pool ", datetime.now().time())
        # self.ranking()
        # top2 = self.population[:(int(0.1 * self.population_size))]  # ELITISM
        self.population = []
        # self.population.extend(top2)
        print(f"Creating GENERATION {self.current_generation}", datetime.now().time())
        self.current_generation += 1
        # while len(self.population) < 1:
        while len(self.population) < self.population_size + (self.population_size * self.growth_rate):
            a_index = random.randrange(len(self.mating_pool))
            b_index = random.randrange(len(self.mating_pool))
            parent_a = (self.mating_pool[a_index])
            parent_b = (self.mating_pool[b_index])
            if parent_a == parent_b:
                continue
            child = parent_a.crossover(parent_b, self.mutation_rate)
            # self.mutation(child)
            self.population.append(child)
            # print(len(self.new_generation))

    def ranking(self):
        copied_population = self.population
        for i in range(len(self.population)):
            for j in range(len(self.population)):
                if (self.population[i].conflicts > self.population[j].conflicts):
                    self.population[i], self.population[j] = self.population[j], self.population[i]

        # print([population.conflicts for population in copied_population])


    def plot(self):
        # fig = plt.figure(figsize=(10, 10))
        plt.style.use("dark_background")
        plt.rcParams["figure.figsize"] = (12, 5) # size of the chart
        # plt.rcParams['toolbar'] = 'None' # removes toolbar at the bottom

        plt.plot(self.plots)
        # plt.plot(self.mutation_count_list)

        for color in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
            plt.rcParams[color] = '#052C30' 
        for color in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
            plt.rcParams[color] = '#E6F9FA'

        plt.grid(color='#2A3459')

        # plt.suptitle('PROPORTIONAL GROWTH RATE', fontsize=22)
        plt.xlabel('Schedules', fontsize=16)
        plt.ylabel('Conflicts', fontsize=16)

        plt.show()