from datetime import time, timedelta
from .schedule import Schedule
from .scheduled_course import ScheduledCourse
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
        self.convnt_avg_vacancy = avg_vacancy
        self.convnt_avg_classes = avg_classes
        self.convnt_avg_class_hrs = avg_class_hrs
        self.convnt_max_consecutive_classes = max_consecutive_classes
        self.convnt_max_consecutive_class_hrs = max_consecutive_class_hrs
        self.convnt_vacancy_session_ratio = self.convnt_avg_vacancy / self.convnt_avg_class_hrs

    @property
    def convnt_avg_dismissal_in_td(self) -> timedelta:
        """Returns the defined most convenient avg dismissal in timedelta"""
        return timedelta(hours=self.convnt_avg_dismissal.hour, minutes=self.convnt_avg_dismissal.minute)

    @staticmethod
    def time_to_td(_time: time):
        """Converts time to timedelta"""
        return timedelta(hours=_time.hour, minutes=_time.minute)

    @staticmethod
    def _get_avg_dismissal(schedule: Schedule) -> timedelta:
        """Returns the average time of the list of time objects passed in timedelta""" 
        dismissals = []
        for val in schedule.schedule.values():
            if (len(val) > 0):
                course: ScheduledCourse
                course = val[-1]
                course_dismissal = Evaluator.time_to_td(course.end_time)
                dismissals.append(course_dismissal)

        # TODO: Needs checking
        avg = (sum([_time.seconds for _time in dismissals]) / 3600) / len(dismissals)
        return timedelta(hours=floor(avg), minutes=(avg % floor(avg)) * 60)

    @staticmethod
    def _get_avg_vacancy(schedule: Schedule) -> int:
        vacants = timedelta()

        val: list[ScheduledCourse]
        for val in schedule.schedule.values():  # for each day of the week's schedule
            print(val)
            if len(val) > 0:
                for i in range(len(val)):   # for every courses in the day's schedule
                    if i < len(val) - 1:
                        vacant = Evaluator.time_to_td(val[i+1].start_time) - Evaluator.time_to_td(val[i].end_time)
                        vacants += vacant
        return vacants

    @staticmethod
    def _get_avg_classes(schedule: Schedule) -> int:
        pass

    @staticmethod
    def _get_avg_class_hrs(schedule: Schedule) -> int:
        pass

    @staticmethod
    def _get_max_consecutive_classes(schedule: Schedule) -> int:
        pass

    @staticmethod
    def _get_max_consecutive_class_hrs(schedule: Schedule) -> int:
        pass

    def evaluate(self, schedule: Schedule):
        """Evaluates the given schedule based on the defined most convenient schedule"""

        # ========== EVALUATION 1: Evaluate the average dismissal ========== #
        sched_avg_dismissal = self._get_avg_dismissal(schedule)
        avg_dismissal_diff = self.convnt_avg_dismissal_in_td - sched_avg_dismissal

        # ========== EVALUATION 2: Evaluate the average vacancy ========== #
        sched_avg_vacancy = self._get_avg_vacancy(schedule)
        # avg_vacancy_diff = self.convnt_avg_vacancy - sched_avg_vacancy

        # # ========== EVALUATION 3: Evaluate the average classes ========== #
        # sched_avg_classes = self._get_avg_classes(schedule)
        # avg_classes_diff = self.convnt_avg_classes - sched_avg_classes

        # # ========== EVALUATION 4: Evaluate the average class hours ========== #
        # sched_avg_class_hrs = self._get_avg_class_hrs(schedule)
        # avg_class_hrs_diff = self.convnt_avg_class_hrs - sched_avg_class_hrs

        # # ========== EVALUATION 5: Evaluate the maximum consecutive classes ========== #
        # sched_max_consecutive_classes = self._get_max_consecutive_classes(schedule)
        # max_consecutive_classes_diff = self.convnt_max_consecutive_classes - sched_max_consecutive_classes

        # # ========== EVALUATION 6: Evaluate the maximum consecutive class hours ========== #
        # sched_max_consecutive_class_hrs = self._get_max_consecutive_class_hrs(schedule)
        # sched_max_consecutive_class_hrs = self.convnt_max_consecutive_class_hrs - sched_max_consecutive_class_hrs

        print(sched_avg_vacancy)