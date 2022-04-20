from enum import Enum
from itertools import combinations
from functools import cmp_to_key

class DayOfWeek(Enum):
    MONDAY = 1,
    TUESDAY = 2,
    WEDNESDAY = 3,
    THURSDAY = 4,
    FRIDAY = 5,
    SATURDAY = 6 
    SUNDAY = 7


class TimetableEntry:
    def __init__(self, day: DayOfWeek, startHour: int, startMinute: int, endHour: int, endMinute: int):
        self.day = day
        self.startMinute = startHour * 60 + startMinute
        self.endMinute = endHour * 60 + endMinute

    def get_intersection_minutes(self, otherEntry):
        if self.day != otherEntry.day:
            return 0
        
        commonStart = max(self.startMinute, otherEntry.startMinute)
        commonEnd = min(self.endMinute, otherEntry.endMinute)
        diff = commonEnd - commonStart
        if diff > 0:
            return diff
        return 0

    def __str__(self):
        startHour = int(self.startMinute / 60)
        startMinute = int(self.startMinute % 60)
        endHour = int(self.endMinute / 60)
        endMinute = int(self.endMinute % 60)
        return f"{self.day.name} {startHour}:{startMinute} - {endHour}:{endMinute}"

    def __repr__(self) -> str:
        return self.__str__()


class Course:

    def __init__(self, name: str, timeSlots, groupId=None, isMandatory=False):
        self.name = name
        self.timeSlots = timeSlots
        self.groupId = groupId
        self.isMandatory = isMandatory

    def __str__(self):
        result = self.name + ": "
        for i in range(len(self.timeSlots)):
            slot = self.timeSlots[i]
            result += str(slot)
            if i < len(self.timeSlots) - 1:
                result += ", "

        return result

    def get_intersection_time(self, otherCourse):
        time = 0
        for slot in self.timeSlots:
            for otherSlot in otherCourse.timeSlots:
                time += slot.get_intersection_minutes(otherSlot)
        return time

def get_combination_intersection_time(combination):
    intersecting_courses = []
    time = 0
    for i in range(len(combination)):
        for j in range(i + 1, len(combination)):
            intersection = combination[i].get_intersection_time(combination[j])
            time += intersection
            if intersection > 0:
                intersecting_courses.append((combination[i], combination[j]))
    return time, intersecting_courses

def get_combination_window_time(combination):
    return 0

def print_combination(combination):
    for course in combination:
        print(course, end=", ")

def validate_combination(combination, mandatoryCourses):
    present_groups = []

    for course in combination:
        if course.groupId is None:
            continue
        if course.groupId in present_groups:
            return False
        present_groups.append(course.groupId)

    for mandatoryCourse in mandatoryCourses:
        if mandatoryCourse not in combination and mandatoryCourse.groupId not in present_groups:
            return False 

    return True                

def combination_comparator(tuple0, tuple1):
    intersectionTime0 = tuple0[1]
    intersectionTime1 = tuple1[1]
    windowTime0 = tuple0[2]
    windowTime1 = tuple1[2]

    if intersectionTime0 < intersectionTime1:
        return -1
    elif intersectionTime0 > intersectionTime1:
        return 1
    else: 
        return windowTime1 - windowTime0

def course_tuple_to_string(course_tuple):
    text = ""
    for course_index in range(len(course_tuple)):
        text += course_tuple[course_index].name
        if course_index < len(course_tuple) - 1:
            text += ", "

    return text

def get_combinations(courses, maxLength, cutoffIntersectionTime=10000):
    mandatory_courses = []
    for course in courses:
        if course.isMandatory:
            mandatory_courses.append(course)

    combs = combinations(courses, maxLength)

    combination_list = []

    for combination in combs:
        if not validate_combination(combination, mandatory_courses):
            continue

        intersection_time, intersecting_courses = get_combination_intersection_time(combination)
        if intersection_time > cutoffIntersectionTime:
            continue

        window_time = get_combination_window_time(combination)
        combination_info = (combination, intersection_time, window_time, intersecting_courses)
        combination_list.append(combination_info)

    combination_list.sort(key = cmp_to_key(combination_comparator))
    return combination_list

courses = [
    Course("Parallel Programming", [
    TimetableEntry(DayOfWeek.THURSDAY, 8, 0, 10, 0),
    TimetableEntry(DayOfWeek.TUESDAY, 8, 0, 11, 0)
    ]),
    #Course("System Security", [
    #TimetableEntry(DayOfWeek.MONDAY, 12, 0, 16, 0),
    #]),
    Course("Graphs", [
    TimetableEntry(DayOfWeek.MONDAY, 10, 0, 12, 0),
    TimetableEntry(DayOfWeek.THURSDAY, 12, 0, 16, 0),
    ]),
    Course("Functional programming", [
    TimetableEntry(DayOfWeek.TUESDAY, 16, 0, 18, 0),
    TimetableEntry(DayOfWeek.WEDNESDAY, 14, 0, 16, 0),
    TimetableEntry(DayOfWeek.THURSDAY, 12, 0, 14, 0),
    ]),
    Course("SW Anal", [
    TimetableEntry(DayOfWeek.TUESDAY, 8, 0, 10, 0),
    TimetableEntry(DayOfWeek.WEDNESDAY, 8, 0, 10, 0),
    TimetableEntry(DayOfWeek.THURSDAY, 12, 0, 14, 0),
    ]),
    Course("Mobile Security", [
    TimetableEntry(DayOfWeek.TUESDAY, 14, 0, 18, 0),
    ]),
    Course("Program Repair", [
    TimetableEntry(DayOfWeek.FRIDAY, 12, 0, 18, 0),
    ]),
    #Course("SW Project Management", [
    #TimetableEntry(DayOfWeek.MONDAY, 16, 0, 18, 0),
    #TimetableEntry(DayOfWeek.THURSDAY, 17, 0, 18, 0),
    #]),
    Course("Responsible Machine Learning", [
    TimetableEntry(DayOfWeek.TUESDAY, 14, 0, 16, 0),
    TimetableEntry(DayOfWeek.THURSDAY, 14, 0, 18, 0),
    ]),
    Course("Computer Linguistics", [
    TimetableEntry(DayOfWeek.THURSDAY, 10, 0, 12, 0),
    TimetableEntry(DayOfWeek.WEDNESDAY, 10, 0, 12, 0),
    ]),
    Course("Critical Infrastructure", [
    TimetableEntry(DayOfWeek.TUESDAY, 14, 0, 18, 0),
    TimetableEntry(DayOfWeek.WEDNESDAY, 16, 0, 18, 0),
    ]),
    Course("Coding Theory", [
    TimetableEntry(DayOfWeek.TUESDAY, 16, 0, 17, 0),
    TimetableEntry(DayOfWeek.WEDNESDAY, 16, 0, 18, 0),
    TimetableEntry(DayOfWeek.THURSDAY, 16, 0, 18, 0),
    ]),
    Course("Planning of Complex...", [
    TimetableEntry(DayOfWeek.MONDAY, 12, 0, 14, 0),
    TimetableEntry(DayOfWeek.TUESDAY, 8, 0, 12, 0),
    ]),

    Course("Probability Theory", [
    TimetableEntry(DayOfWeek.WEDNESDAY, 16, 0, 18, 0),
    TimetableEntry(DayOfWeek.THURSDAY, 10, 0, 12, 0),
    TimetableEntry(DayOfWeek.FRIDAY, 16, 0, 18, 0),
    ]),
    Course("Statistics", [
    TimetableEntry(DayOfWeek.WEDNESDAY, 14, 0, 16, 0),
    TimetableEntry(DayOfWeek.THURSDAY, 14, 0, 16, 0),
    ]),
    Course("Machine Learning, Control and Optimization", [
    TimetableEntry(DayOfWeek.FRIDAY, 16, 0, 18, 0),
    TimetableEntry(DayOfWeek.FRIDAY, 8, 0, 10, 0),
    TimetableEntry(DayOfWeek.THURSDAY, 14, 0, 16, 0),
    ]),

    Course("Effective Algs", [
    TimetableEntry(DayOfWeek.MONDAY, 12, 0, 14, 0),
    TimetableEntry(DayOfWeek.TUESDAY, 12, 0, 18, 0),
    ]),

    Course("Deutsch 1", [
    TimetableEntry(DayOfWeek.TUESDAY, 8, 0, 10, 0),
    TimetableEntry(DayOfWeek.THURSDAY, 8, 0, 10, 0),    
    ], groupId=1, isMandatory=True),
    Course("Deutsch 2", [
    TimetableEntry(DayOfWeek.TUESDAY, 10, 0, 12, 0),
    TimetableEntry(DayOfWeek.THURSDAY, 10, 0, 12, 0),
    ], groupId=1, isMandatory=True),
    Course("Deutsch 3", [
    TimetableEntry(DayOfWeek.MONDAY, 12, 0, 14, 0),
    TimetableEntry(DayOfWeek.FRIDAY, 12, 0, 14, 0),
    ], groupId=1, isMandatory=True),
    Course("Deutsch 4", [
    TimetableEntry(DayOfWeek.MONDAY, 14, 0, 16, 0),
    TimetableEntry(DayOfWeek.FRIDAY, 14, 0, 16, 0),
    ], groupId=1, isMandatory=True),
]

print(f"Courses number: {len(courses)}")

combination_infos = get_combinations(courses, 6, 60)

print(f"Filtered combinations number: {len(combination_infos)}")

number_to_print = len(combination_infos)

with open("Output.txt", "w") as f:
    for i in range(len(combination_infos)):
        combination_info = combination_infos[i]
        for course in combination_info[0]:
            f.write(str(course))
            f.write("\n")

        f.write(f"Intersection Time: {combination_info[1]} minutes\n")
        #f.write(f"Window Time: {combination_info[2]} minutes\n")
        if combination_info[3]:
            f.write(f"Intersections: ")
            for course_tuple in combination_info[3]:
                f.write(f"[{course_tuple_to_string(course_tuple)}] ")
            f.write("\n")
        f.write("\n")

        number_to_print -= 1
        if number_to_print <= 0:
            break

