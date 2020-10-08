from __future__ import annotations
from typing import Tuple
from app.models import CourseSection, Instructor, Student
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class ScheduledCourseSection(CourseSection):
    semester: str
    schedule: str  # TODO this maybe should be like, a date time? definitely not a string.
    instructors: Tuple[Instructor]
    registered_students: Tuple[
        Student
    ]  # maybe should keep registered students mutable?
    course_registration_number: str
