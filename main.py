from scheduling import *
from _config import get_course
from datetime import time
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
    scheds = load_csv("scheds.csv")
    evaluator = Evaluator(time(19, 0), 1.5, 5, 6, 2, 5)
    evaluator.evaluate(scheds[2], avg_dismissal_debug=True)

