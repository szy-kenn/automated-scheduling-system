'''
    A - TechDoc (Divided)
    A - TechDoc (Divided)
    B - ArtApp (LEC)
    C - PEco (LEC)
    D - Free Elective (LEC)
    E - DesAlgo (LEC)
    F - PE (LEC)
    G - OS (LEC)
    H - OS (LAB)
    I - IM (LEC)
    J - IM (LAB)

    00000 - None
    00001 - TechDoc
    10001  - ArtApp
    0010 - PEco
    00101 - OS Lec
    10101 - OS Lab
'''
import random
import datetime
import matplotlib.pyplot as plt
from copy import deepcopy

class Genetic:
    def __init__(self, popsize, mutrate, maxgen, selection_pressure) -> None:
        self.popsize = popsize
        self.mutrate = mutrate
        self.maxgen = maxgen
        self.selection_pressure = selection_pressure

        self.courses = ['A', 'A', 'B',
                        'C', 'D', 'E',
                        'F', 'G', 'H',
                        'I', 'J']
        
        self.population = []
        self.lunch_break_indices = [2, 3, 12, 13, 22, 23, 32, 33, 42, 43, 52, 53]
        self.avg_conflict = 0
        self.plots = []
        self.minimum_conflicts = float('inf')

    def print(self, schedule):
        timeslots = ["7:30 AM - 9:00 AM", "9:00 AM - 10:30 AM", "10:30 AM - 12:00 NN",
                     "12:00 NN - 1:30 PM", "1:30 PM - 3:00 PM", "3:00 PM - 4:30 PM",
                     "4:30 PM - 6:00 PM", "6:00 PM - 7:30 PM", "7:30 PM - 9:00 PM"]
        
        course_dict = {
            'A': 'COMP 20113: Technical Documentation',
            'B': 'Art Appreciation',
            'C': "People and the Earth's Ecosystem",
            'D': 'CS Free Elective 2',
            'E': "Design and Analysis of Algorithms",
            'F': "Team Sports",
            'G': "Operating System (LEC)",
            'H': "Operating System (LAB)",
            'I': "Information Management (LEC)",
            'J': "Information Management (LAB)",
            '0': "None"
        }

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        for day_idx in range(0, len(schedule), 10):
            print(f"{days[day_idx//10]}")
            timeslot_idx = 0
            while timeslot_idx < 9:
                print(f"{timeslots[timeslot_idx]}:\t{course_dict[schedule[day_idx+timeslot_idx]]}")
                timeslot_idx += 1
        # for idx, timeslot in enumerate(schedule):
        #     print(f"{days[idx%10]}")
        #     print(f"{timeslots[idx]}: {course_dict[timeslot]}")
            
    def start_world(self):
        _start_time = datetime.datetime.now().time()
        # while self.minimum_conflicts > 0:
        print("Starting World...")
        self.initialize()
        for i in range(self.maxgen):
            # print(f"Generation {i+1}")
            res = self.selection()
            if res:
                break
        self.evaluation()
        self.plot()
        _end_time = datetime.datetime.now().time()
        print(f"Start: {_start_time}, End: {_end_time}")
        return 
    
    def initialize(self):
        for i in range(self.popsize):
            # 9 timeslots + 1 boundary "1" in Monday - Friday
            schedule = ["0" if (i not in (9, 19, 29, 39, 49, 59)) else "1" for i in range(60)]
            added_courses = 0
            while added_courses < 11:
                random_timeslot = random.randrange(0, 54)
                if schedule[random_timeslot] == "0":
                    random_course = random.choice(self.courses)
                    # INSERT COURSE
                    if random_course == "A":
                        schedule[random_timeslot] = random_course
                    else:
                        if schedule[random_timeslot+1] == "0":
                            schedule[random_timeslot] = random_course
                            schedule[random_timeslot+1] = random_course
                        else:
                            continue

                    added_courses += 1
            self.population.append(schedule)
            # print("".join(schedule))
    
    def calculate_fitness(self, schedule: list, _print=False):
        conflicts = 0
        
       # HARD CONSTRAINTS
        # for course in self.courses:
        #     if course not in ("0", "1"):
        #         if course in ('A', 'B'):
        #             if schedule.count(course) > 1:
        #                 conflicts += 20 * (schedule.count(course) - 1)
        #         else:
        #             if schedule.count(course) > 2:
        #                 conflicts += 20 * (schedule.count(course) - 2) / 2
        

        # ascii code - 65 (A (65 - 65) = 0 index)
        all_classes_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        all_day_classes = [True, True, True, True, True, True]
        day_classes_count = [0, 0, 0, 0, 0, 0]

        # SOFT CONSTRAINTS

        # lunch break
        for i in range(0, len(self.lunch_break_indices), 2):
            # print(f"{i}: {schedule[self.lunch_break_indices[i]]} | {i+1}: {schedule[self.lunch_break_indices[i+1]]}")
            if schedule[self.lunch_break_indices[i]] != "0" and schedule[self.lunch_break_indices[i+1]] != "0":
                if _print:
                    print("No lunch break", 10)
                conflicts += 10

        for idx, timeslot in enumerate(schedule):
            if idx == 0:
                classes = 0
                lab = {'H': None, 'J': None}
            
            # if start of day
            if idx%10 == 0 and idx != 0:
                classes = 0

            # if end of day
            if timeslot == "1":
                if classes > 6:
                    if _print:
                        print("+3 classes", 4)
                    conflicts += 4

            # count classes per day
            if timeslot != "0" and timeslot != "1":
                classes += 1
                all_classes_count[ord(timeslot) - 65] += 1
                all_day_classes[int(idx//10)] = False
                day_classes_count[int(idx//10)] += 1

            # lab day constraint
            if timeslot in ("H", "J"):
                lab[timeslot] = int(idx//10)

            # last class
            if timeslot != "1" and schedule[idx+1] == "1":
                if timeslot != "0":
                    # if lab or PE
                    if timeslot in ("F", "H", "J"):
                        if _print:
                            print("lab/pe last class", 5)
                        conflicts += 5
                    else:
                        if _print:
                            print("may klase sa gabi", 3)
                        conflicts += 3           

        # free day constraint
        if not any(all_day_classes):
            if _print:
                print("walang free day", 2)
            conflicts += 2

        # lab constraint
        if lab['H'] == None or lab['J'] == None:
            if _print:
                print("No lab", 8)
            conflicts += 8
        elif lab['H'] != lab['J']:
            if _print:
                print("Di sabay", 8)
            conflicts += 8
            if day_classes_count[lab['H']] > 2:
                conflicts += 5
            if day_classes_count[lab['J']] > 2:
                conflicts += 5
        else:
            if day_classes_count[lab['H']] > 4:
                conflicts += 10

        # HARD CONSTRAINTS
        for idx, class_count in enumerate(all_classes_count):
            if class_count > 2:
                if _print:
                    print("leb/lab duplicate", 20 * (class_count - 2) / 2)
                conflicts += 20 * (class_count - 2) / 2
            elif class_count == 0 or class_count == 1:
                if _print:
                    print("kulang", 20)
                conflicts += 20

        # print(all_classes_count)
        return int(conflicts)
 
    def get_mating_probability(self, conflicts):
        return (200 - conflicts)

    def get_avg_conflicts(self):
        conflicts = 0
        for sched in self.population:
            conflicts += self.calculate_fitness(sched)
        return conflicts / self.popsize
    
    def get_highest_fitness(self, participants): 

        for i in range(len(participants)):
            current = participants[i]
            j = i - 1
            while j >= 0:
                current_participant_conflict = self.calculate_fitness(self.population[current])
                next_participant_conflict = self.calculate_fitness(self.population[participants[j]])
                # print(current_participant_conflict)
                # print(next_participant_conflict)
                # self.plots.append(current_participant_conflict)
                if current_participant_conflict == 0:
                    print(self.population[current])
                    return "0"
                if next_participant_conflict == 0:
                    print(self.population[participants[j]])
                    return "0"
                if next_participant_conflict > current_participant_conflict:
                    participants[j+1] = participants[j]
                    j = j - 1
                else:
                    break
            participants[j+1] = current

        # min = float('inf')
        # min_idx = 0
        # for sched_idx in participants:
        #     conflicts = self.calculate_fitness(self.population[sched_idx])
        #     # print(conflicts)
        #     if conflicts < min:
        #         min = conflicts
        #         min_idx = sched_idx

        return (participants[0], participants[1])

    def selection(self):
        
        new_population = []
        self.plots.append(self.get_avg_conflicts())
        # new_population.extend(top_scheds)
        
        while len(new_population) < self.popsize:

            participants = []

            # tournament
            while len(participants) < self.selection_pressure:
                participants.append(random.randrange(len(self.population)))

            parents = self.get_highest_fitness(participants)
            if parents == "0":
                return True
            parent_a_idx = parents[0]
            parent_b_idx = parents[1]

            # participants = []

            # tournament
            # while len(participants) < self.selection_pressure:
            #     participants.append(random.randrange(len(self.population)))

            # parent_b_idx = random.randrange(len(self.population))

            child = self.crossover(parent_a_idx, parent_b_idx)
            new_population.append(child)    

            child2 = self.crossover(parent_b_idx, parent_a_idx)
            new_population.append(child2)
            # new_population.append(self.population[parent_a_idx])
            # new_population.append(self.population[parent_b_idx])

        self.population = new_population

        # self.mating_pool = []
        # for idx, schedule in enumerate(self.population):
        #     conflicts = self.calculate_fitness(schedule)
        #     # print(conflicts)
        #     # print("".join(schedule))
        #     if conflicts == 0:
        #         courses = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        #         for course in courses:
        #             print(f"{course} {schedule.count(course)}")
        #         print("".join(schedule))
        #         print(conflicts)
        #         return True
        #     for i in range(self.get_mating_probability(conflicts)):
        #         self.mating_pool.append(idx)

        # self.ranking()
        # top_scheds = self.population[:int(0.1 * self.popsize)]

    def crossover(self, parent_a, parent_b):
        midpoint = random.choice([9, 19, 29, 39, 49])
        # print(midpoint)
        child = []
        child.extend(deepcopy( self.population[parent_a][:midpoint] ))
        child.extend(deepcopy( self.population[parent_b][midpoint:] ))
        # print("================")
        # print("".join(self.population[parent_a][:midpoint]))
        # print("".join(self.population[parent_b][midpoint:]))
        # print("".join(child))
        child = self.mutation(child)
        return child
    
    def mutation(self, child):
        
        def _mutate(course, space):
            if space == 1:
                random_mutation = random.random()
                if random_mutation <= self.mutrate:
                    flip_coin = random.randint(0, 1)
                    if flip_coin == 0:
                        return ("0", 1)
                    else:
                        new_course = "A"
                        return (new_course, 1)
                else:
                    return (course, space)
                    
            else:
                random_mutation = random.random()
                if random_mutation <= self.mutrate:
                    random_choice = random.random()
                    if random_choice <= 0.083:
                        return ("0", 1)
                    else:
                        random_course = random.choice(self.courses)
                        return (random_course, (1 if random_course == "A" else 2))
                else:
                    return (course, space)
                
        for idx in range(0, len(child), 10):

            timeslot_idx = 0
            
            while timeslot_idx < 9:
                schedule_idx = idx + timeslot_idx

                if child[schedule_idx] == "0" or child[schedule_idx] == "A":
                    if child[schedule_idx+1] == "0":
                        mutated_timeslot = _mutate(child[schedule_idx], 2)
                        if mutated_timeslot[1] == 1:
                            child[schedule_idx] = mutated_timeslot[0]
                            child[schedule_idx+1] = "0"
                        else:
                            child[schedule_idx] = mutated_timeslot[0]
                            child[schedule_idx+1] = mutated_timeslot[0]
                            timeslot_idx += 1
                    else:
                        mutated_timeslot = _mutate(child[schedule_idx], 1)
                        child[schedule_idx] = mutated_timeslot[0]
                else:
                    mutated_timeslot = _mutate(child[schedule_idx], 2)
                    if mutated_timeslot[1] == 1:
                        child[schedule_idx] = mutated_timeslot[0]
                        child[schedule_idx+1] = "0"
                    else:
                        child[schedule_idx] = mutated_timeslot[0]
                        child[schedule_idx+1] = mutated_timeslot[0]
                        timeslot_idx += 1
                
                timeslot_idx += 1

        return child

    def evaluation(self):
        
        min = float('inf')
        min_idx = 0

        for i in range(len(self.population)):
            conflicts = self.calculate_fitness(self.population[i])
            if conflicts < min:
                min = conflicts
                min_idx = i

        # for i in range(len(self.population)):
        #     for j in range(len(self.population)):
        #         if self.calculate_fitness(self.population[i]) < self.calculate_fitness(self.population[j]):
        #             self.population[i], self.population[j] = self.population[j], self.population[i]
        self.minimum_conflicts = min
        print(min)
        self.calculate_fitness(self.population[min_idx], True)
        print("".join(self.population[min_idx]))
        self.print(self.population[min_idx])

    def elitism(self):
        pass

    def clone(self, schedule, num):
        pass        

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

# genetic = Genetic(2000, 0.0125, 100, 5)
# genetic.start_world()

# genetic = Genetic(200, 0.01, 100, 5)
# genetic.start_world()