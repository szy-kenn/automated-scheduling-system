from classes.course import Course
from config import *
import csv

courses = []
with open ("scheds.csv", "r") as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        courses.append(course)

# print([course for course in courses])
