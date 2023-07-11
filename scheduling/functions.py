from datetime import datetime, time, timedelta

def debug_bracket():
    return f"[DEBUG {datetime.now().time().strftime('%H:%M:%S')}]"

def sec_to_time(_sec: int) -> time:
    """Converts seconds to time object"""

    _hour = int(_sec // 3600)
    _min = int((_sec % 3600) // 60)
    return time(hour=_hour, minute=_min)

def time_to_sec(_time: time) -> int:
    """Converts time to seconds"""
    return _time.hour * 3600 + _time.minute * 60

def time_to_td(_time: time) -> timedelta:
    """Converts time to timedelta"""

    return timedelta(hours=_time.hour, minutes=_time.minute)

def td_to_time(_td: timedelta) -> time:
    """Converts timedelta to time"""

    return time(hour=int(_td.seconds / 3600), minute=int(_td.seconds % 3600 / 60))

def get_course_sched(course, sched_list: list) -> list:
    """Returns the schedule of the given course in every sections
    
    Parameters
    ----------
    course : Course
        Course object
    sched_list : list[Schedule]
        a list of Schedule object
    """

    _course_sched = {}

    for sched in sched_list:
        _course_sched[sched.name] = [] 
        for timeslot_container in sched.schedule.values():
            if len(timeslot_container.assigned_timeslots) > 0:
                for timeslot in timeslot_container.assigned_timeslots:
                    if timeslot.course.code == course.code:
                        _tuple = (timeslot.course.start_time.strftime("%H:%M:%S"), timeslot.course.day)
                        if not _tuple in _course_sched[sched.name]:
                            _course_sched[sched.name].append(_tuple)

    for key, val in _course_sched.items():
        print(key)
        for pair in val:
            print(f"{pair[0]} - {pair[1]}")
    # return _course_sched