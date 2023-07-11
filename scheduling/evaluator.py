from .schedule import Schedule
from .scheduled_course import ScheduledCourse
from .functions import _debug_bracket
from datetime import time, timedelta
from copy import deepcopy
from math import floor

class Evaluator:

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

    @staticmethod
    def sec_to_time(_sec: int) -> time:
        """Converts seconds to time object"""

        _hour = int(_sec // 3600)
        _min = int((_sec % 3600) // 60)
        return time(hour=_hour, minute=_min)
    
    @staticmethod
    def time_to_sec(_time: time) -> int:
        """Converts time to seconds"""
        return _time.hour * 3600 + _time.minute * 60

    @staticmethod
    def time_to_td(_time: time):
        """Converts time to timedelta"""

        return timedelta(hours=_time.hour, minutes=_time.minute)

    @staticmethod
    def _get_avg_dismissal(schedule: Schedule, debug=False) -> int:
        """Returns the average time of the list of time objects passed in seconds""" 

        dismissals = []
        if debug:
            print(f"{_debug_bracket()} Evaluating Average Dismissal...")
        for val in schedule.schedule.values():  # val type : list[ScheduledCourse]
            if (len(val) > 0):
                course: ScheduledCourse
                course = val[-1]
                course_dismissal = Evaluator.time_to_td(course.end_time)
                if debug:
                    print(f"{_debug_bracket()} Getting dismissal time on {course.day}\t: {course_dismissal}")
                dismissals.append(course_dismissal)

        # TODO: Needs checking
        avg = sum([_time.seconds for _time in dismissals]) / len(dismissals)
        # td_avg = timedelta(hours=floor(avg), minutes=(avg % floor(avg)) * 60)
        if debug:
            print(f"{_debug_bracket()} Computed dismissal time: {avg}")
        return avg

    @staticmethod
    def _get_avg_vacancy(schedule: Schedule, debug=False) -> time:
        """Returns the average vacancy of the schedule for the whole week in seconds"""

        vacants = timedelta()
        counter = 0

        val: list[ScheduledCourse]
        for val in schedule.schedule.values():  # for each day of the week's schedule
            if len(val) > 0:
                for i in range(len(val)):   # for every courses in the day's schedule
                    if i < len(val) - 1:
                        vacant = Evaluator.time_to_td(val[i+1].start_time) - Evaluator.time_to_td(val[i].end_time)
                        vacants += vacant
                        counter += 1
        return vacants.seconds / counter

    @staticmethod
    def _get_avg_classes(schedule: Schedule, debug=False) -> int:
        # WAG NA TO
        total_counter = 0

        for val in schedule.schedule.values():
            counter = 0
            if (len(val) > 0):
                for course in val:
                    counter += 1
                total_counter += counter
                print(f"{course.day}", counter)
        print(f"{total_counter / 6}")
        
    @staticmethod
    def _get_avg_class_hrs(schedule: Schedule, debug=False) -> int:
        pass

    @staticmethod
    def _get_max_consecutive_classes(schedule: Schedule, debug=False) -> int:
        pass

    @staticmethod
    def _get_max_consecutive_class_hrs(schedule: Schedule, debug=False) -> int:
        for key, val in schedule.schedule.items():
            if len(val) > 0:
                max_consecutive_secs = 0
                i = 0
                start_time = time()
                end_time = time()
                while i < len(val) -1:
                    while (i < len(val) - 1 and 
                            Evaluator.time_to_sec(val[i].end_time) == Evaluator.time_to_sec(val[i+1].start_time)):
                        if start_time.hour == 0:
                            start_time = val[i].start_time
                        i += 1
                        end_time = val[i].end_time
                        if Evaluator.time_to_sec(end_time) - Evaluator.time_to_sec(start_time) > max_consecutive_secs:
                            max_consecutive_secs = Evaluator.time_to_sec(end_time) - Evaluator.time_to_sec(start_time)
                    i += 1
                max_consecutive_hrs = max_consecutive_secs / 3600
                print(max_consecutive_hrs)

    def evaluate(self, schedule: Schedule, **kwargs):
        """Evaluates the given schedule based on the defined most convenient schedule"""

        # ========== EVALUATION 1: Evaluate the average dismissal ========== #
        sched_avg_dismissal = self._get_avg_dismissal(schedule, debug=kwargs.get('avg_dismissal_debug') if kwargs.get('avg_dismissal_debug') != None else False)
        avg_dismissal_diff = (self.time_to_sec(self.convnt_avg_dismissal) - sched_avg_dismissal) / 3600

        # ========== EVALUATION 2: Evaluate the average vacancy ========== #
        sched_avg_vacancy = self._get_avg_vacancy(schedule)
        avg_vacancy_diff = (self.convnt_avg_vacancy - sched_avg_vacancy) / 3600

        # # ========== EVALUATION 3: Evaluate the average classes ========== #
        # sched_avg_classes = self._get_avg_classes(schedule)
        # avg_classes_diff = self.convnt_avg_classes - sched_avg_classes

        # # ========== EVALUATION 4: Evaluate the average class hours ========== #
        # sched_avg_class_hrs = self._get_avg_class_hrs(schedule)
        # avg_class_hrs_diff = self.convnt_avg_class_hrs - sched_avg_class_hrs

        # ========== EVALUATION 5: Evaluate the maximum consecutive classes ========== #
        sched_max_consecutive_classes = self._get_max_consecutive_classes(schedule)
        max_consecutive_classes_diff = self.convnt_max_consecutive_classes - sched_max_consecutive_classes

        # # ========== EVALUATION 6: Evaluate the maximum consecutive class hours ========== #
        # sched_max_consecutive_class_hrs = self._get_max_consecutive_class_hrs(schedule)
        # sched_max_consecutive_class_hrs = self.convnt_max_consecutive_class_hrs - sched_max_consecutive_class_hrs

        print(f"Dismissal Difference: {avg_dismissal_diff} hrs\nVacancy Difference: {avg_vacancy_diff} hrs\nMax Consecutive Classes{max_consecutive_classes_diff}")
    
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