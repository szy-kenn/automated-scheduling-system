from scheduling.course import Course
from typing import Final

COMP20093: Final = Course('COMP', 20093, 'Information Management', True, 3, 2)
COMP20103: Final = Course('COMP', 20103, 'Operating System', True, 3, 2)
COMP20113: Final = Course('COMP', 20113, 'Technical Documentation', False, 0, 3)
COSC30033: Final = Course('COSC', 30033, 'Design and Analysis of Algorithms', False, 0, 3)
COSCFE2: Final   = Course('COSC', "FE2", 'CS Free Elective 2', False, 0, 3)
GEED10073: Final = Course('GEED', 10073, 'Art Appreciation', False, 0, 3)
GEED20113: Final = Course('GEED', 20113, "People and the Earth's Ecosystem", False, 0, 3)
PHED10042: Final = Course('PHED', 10042, "Team Sports", False, 0, 2)

defined_courses = [COMP20093, COMP20103, COMP20113, COSC30033, COSCFE2, GEED10073, GEED20113, PHED10042]

def get_course(course_code):
    """Returns the Course object given the course code"""
    for course in defined_courses:
        if course.code == course_code:
            return course
