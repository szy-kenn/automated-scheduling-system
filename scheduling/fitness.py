from .schedule import Schedule
from .scheduled_course import ScheduledCourse
from .functions import *
from ._config import *
from datetime import time, timedelta
from copy import deepcopy
from math import floor

class Fitness:

    def __init__(self, avg_dismissal: time, avg_vacancy: int, avg_classes: int,
                 avg_class_hrs: int, max_consecutive_classes: int,  max_consecutive_class_hrs: int) -> None:
        """
        Initialization for the Evaluator class
        
        All "convnt"-prefixed attributes are the defined most convenient values for
        the certain factor
        """

        self.convnt_avg_dismissal = avg_dismissal
        self.convnt_avg_vacancy = avg_vacancy * 3600
        self.convnt_avg_classes = avg_classes
        self.convnt_avg_class_hrs = avg_class_hrs
        self.convnt_max_consecutive_classes = max_consecutive_classes
        self.convnt_max_consecutive_class_hrs = max_consecutive_class_hrs
        self.convnt_vacancy_session_ratio = self.convnt_avg_vacancy / self.convnt_avg_class_hrs

    def get_true_score(self, initial_score, c=0) -> float:
        # avg_dismissal = self._get_avg_dismissal(schedule)
        # initial_score = avg_dismissal / time_to_sec(self.convnt_avg_dismissal)

        if initial_score <= 1:
            final_score = initial_score / 1
        else:
            final_score = (1 / initial_score) - (1 - (1/initial_score * (1-c)))

        if final_score < 0:
            return 0
        return final_score
    
    def get_overall_score(self, dismissal, vacancy, consecutive_hrs):
        total = dismissal * 0.4 + vacancy * 0.3 + consecutive_hrs * 0.3
        return total 

    def _get_avg_dismissal_score(self, schedule: Schedule, debug=False) -> int:
        """Returns the average time of the list of time objects passed in seconds""" 

        dismissals = []
        if debug:
            print(f"{debug_bracket()} Evaluating Average Dismissal...")
        for timeslot_container in schedule.schedule: 
            if (len(timeslot_container.assigned_timeslots) > 0):
                course: ScheduledCourse
                course = timeslot_container.assigned_timeslots[-1].course
                course_dismissal = time_to_td(course.end_time)
                if debug:
                    print(f"{debug_bracket()} Getting dismissal time on {course.day}\t: {course_dismissal}")
                dismissals.append(course_dismissal)

        # TODO: Needs checking
        avg = sum([_time.seconds for _time in dismissals]) / len(dismissals)
        # td_avg = timedelta(hours=floor(avg), minutes=(avg % floor(avg)) * 60)
        if debug:
            print(f"{debug_bracket()} Computed dismissal time: {avg}")
        return avg / time_to_sec(self.convnt_avg_dismissal)
    
    def _get_avg_vacancy_score(self, schedule: Schedule, debug=False) -> time:
        """Returns the average vacancy of the schedule for the whole week in seconds"""

        vacants = timedelta()
        counter = 0

        for timeslot_container in schedule.schedule:  # for each day of the week's schedule
            if len(timeslot_container.assigned_timeslots) > 0:
                for i in range(len(timeslot_container.assigned_timeslots)):   # for every courses in the day's schedule
                    if i < len(timeslot_container.assigned_timeslots) - 1:
                        vacant = time_to_td(timeslot_container.assigned_timeslots[i+1].course.start_time) - time_to_td(timeslot_container.assigned_timeslots[i].course.end_time)
                        vacants += vacant
                        counter += 1
        return (vacants.seconds / counter) / self.convnt_avg_vacancy

    def _get_avg_classes(self, schedule: Schedule, debug=False) -> int:
        # WAG NA TO
        total_counter = 0

        for val in schedule.schedule:
            counter = 0
            if (len(val) > 0):
                for course in val:
                    counter += 1
                total_counter += counter
                print(f"{course.day}", counter)
        print(f"{total_counter / 6}")
        
    def _get_avg_class_hrs(self, schedule: Schedule, debug=False) -> int:
        pass

    def _get_max_consecutive_classes(self, schedule: Schedule, debug=False) -> int:
        pass

    def _get_max_consecutive_class_hrs_score(self, schedule: Schedule, debug=False) -> int:
        max_consecutive_hrs_per_day = []
        for idx, timeslot_container in enumerate(schedule.schedule):
            if len(timeslot_container.assigned_timeslots) > 0:
                max_consecutive_secs = 0
                i = 0
                start_time = time()
                end_time = time()
                while i < len(timeslot_container.assigned_timeslots) -1:
                    while (i < len(timeslot_container.assigned_timeslots) - 1 and 
                            time_to_sec(timeslot_container.assigned_timeslots[i].course.end_time) == time_to_sec(timeslot_container.assigned_timeslots[i+1].course.start_time)):
                        if start_time.hour == 0:
                            start_time = timeslot_container.assigned_timeslots[i].course.start_time
                        i += 1
                        end_time = timeslot_container.assigned_timeslots[i].course.end_time
                        if time_to_sec(end_time) - time_to_sec(start_time) > max_consecutive_secs:
                            max_consecutive_secs = time_to_sec(end_time) - time_to_sec(start_time)
                    i += 1
                max_consecutive_hrs = max_consecutive_secs / 3600
                max_consecutive_hrs_per_day.append(max_consecutive_hrs)
        return max(max_consecutive_hrs_per_day) / self.convnt_max_consecutive_class_hrs
        # return sum(max_consecutive_hrs_per_day) / len(max_consecutive_hrs_per_day)

    def evaluate(self, schedule: Schedule, **kwargs):
        """Evaluates the given schedule based on the defined most convenient schedule"""
        
        conflict = 0

        # HARD CONSTRAINTS
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
        
        for individual in individuals:
            if schedule.get_course(individual) == -1:
                conflict += 15

        # may lunch break ka ba?
        for timeslot_container in schedule.schedule:
            if (timeslot_container.container[timeslot_container.get_timeslot(time(hour=10, minute=30))].course != None
                and timeslot_container.container[timeslot_container.get_timeslot(time(hour=12))].course != None):
                conflict += 1

        # may free day ka ba?
        class_day_counter = 0
        for timeslot_container in schedule.schedule:
            if len(timeslot_container.assigned_courses) > 0:
                class_day_counter += 1

        if class_day_counter == 6:
            conflict += 1
        
        # ano oras uwian mo?
        for timeslot_container in schedule.schedule:
            if timeslot_container.assigned_timeslots:
                # last_timeslot = timeslot_container.assigned_timeslots[len(timeslot_container.assigned_timeslots)-1]
                last_timeslot = timeslot_container.container[timeslot_container.get_timeslot(time(hour=19, minute=30))].course
                if (last_timeslot != None):
                    conflict += 1
                    # LAB ba yan?
                    if last_timeslot.type == "PHED 10042":
                        conflict += 2
        
        # maximum classes
        for timeslot_container in schedule.schedule:
            if len(timeslot_container.assigned_courses) > 3:
                conflict += 1
            # elif len(timeslot_container.assigned_courses) == 0:
            #     conflict -= 1

        # magkahiwalay ba lab subjects mo? may kasama ba syang iba?
        lab_sub_day = None
        for timeslot_container in schedule.schedule:
            for assigned_courses in timeslot_container.assigned_courses:
                if assigned_courses.type == 'LAB':
                    if assigned_courses.start_time.hour >= 18:
                        conflict += 2
                    if lab_sub_day == None:
                        lab_sub_day = assigned_courses.day
                    else:
                        if lab_sub_day != assigned_courses.day:
                            conflict += 1
                            if len(schedule.get_by_day(lab_sub_day).assigned_courses) > 1:
                                conflict += 1
                            if len(schedule.get_by_day(assigned_courses.day).assigned_courses) > 1:
                                conflict += 1
                        else:
                            if len(schedule.get_by_day(lab_sub_day).assigned_courses) > 2:
                                conflict += 2

        return conflict     


        # lego formula
        # dismissal_score = self._get_avg_dismissal_score(schedule)
        # vacancy_score = self._get_avg_vacancy_score(schedule)
        # max_consecutive_score = self._get_max_consecutive_class_hrs_score(schedule)
        # overall_score = self.get_overall_score(dismissal_score, vacancy_score, max_consecutive_score)
        # return overall_score

    # def swap(self, arr, i1, i2):
    #     copied = deepcopy(arr)
    #     temp = copied[i1]
    #     copied[i1] = copied[i2]
    #     copied[i2] = temp
    #     return copied   

    # def switch_scheds(self, schedule: Schedule):
    #     permutations = []
    #     operation = 0
    #     best_eval = float('-inf')

    #     def permutation(array, left):
    #         nonlocal best_eval, operation

    #         if ((len(array)-1) - left == 0):
    #             operation += 1
    #             permutations.append(array)

    #             # if self.sum_arr(array) < minimum:
    #             #     minimum = self.sum_arr(array)
    #             #     best_assignment = array

    #             return array
            
    #         for i in range(left, len(array)):
    #             swapped = self.swap(array, i, left)
    #             permutation(swapped, left+1)

    #     permutation(schedule, 0)