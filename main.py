from scheduling import *
from datetime import time
from tabulate import tabulate
import csv

def get_time(str):
    hour = int(str[:str.index(":")])
    if str[-2:].lower() == 'pm' and hour < 12:
        hour += 12
    min = int(str[str.index(":")+1:str.index(":")+3])
    return (hour, min)

def load_csv(csv_path):
    """Loads the given csv file and returns a list of six sublists
        containing the schedule of the corresponding sublists (sections)"""
    cs21 = Schedule('BSCS 2-1')
    cs22 = Schedule('BSCS 2-2')
    cs23 = Schedule('BSCS 2-3')
    cs24 = Schedule('BSCS 2-4')
    cs25 = Schedule('BSCS 2-5')
    cs21n = Schedule('BSCS 2-1N')

    with open (csv_path, "r", encoding='utf-8-sig') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            scheduled_course = ScheduledCourse(get_course(row[4]), row[1], time(*get_time(row[2])), time(*get_time(row[3])))
            match row[0]:
                case 'CS2-1':
                    cs21.add_course(scheduled_course)
                case 'CS2-2':
                    cs22.add_course(scheduled_course)
                case 'CS2-3':
                    cs23.add_course(scheduled_course)
                case 'CS2-4':
                    cs24.add_course(scheduled_course)
                case 'CS2-5':
                    cs25.add_course(scheduled_course)
                case 'CS2-1N':
                    cs21n.add_course(scheduled_course)

    return [cs21, cs22, cs23, cs24, cs25, cs21n]

if __name__ == '__main__':
    # pop = Population()
    genetic = Genetic(100, 0, 0.008, 200, time(21, 0), 1.5, 5, 6, 2, 3)

    scheds = []
    conflicts = []

    genetic.start_world()

    # for i in range(100):
    #     # print(f"{i} Formulating the best schedule...")
    #     pop.population = pop.create_individuals()
    #     conflict = genetic.evaluate(pop.population)
    #     # if score == 0:
    #     #     pop.population.print()
    #     #     break
    #     scheds.append(pop.population)
    #     conflicts.append(conflict)
    #     print(f"{i} | {fitness.evaluate(pop.population)}")
    # print(conflicts.index(max(conflicts)))
    
    # with open("random_data.csv", "w", encoding="UTF8", newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["SCHEDULE NO.", "DISMISSAL SCORE", "VACANCY SCORE", "MAX CONSC CLASS", "TRUE SCORE"])
    #     for item in _list:
    #         writer.writerow(item)

    # scheds = load_csv("scheds.csv")
    # s = scheds[0]
    # lego_stacker = LegoStacker()

    # lego_stacker.initialize()
    # # lego_stacker.create_baseplate()
    # res = lego_stacker.place([COMP20093, COMP20103])
    # print(res)
    # print(s.schedule[0].assigned_courses)

    # s.change_timeslot(s.schedule[0].assigned_courses[1], s.schedule[0].container[22], 'Monday')
