from __future__ import annotations
from typing import Tuple
from escore.models import CourseSection
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from rdflib import URIRef


@dataclass_json
@dataclass(frozen=True)
class ScheduledCourseSection(CourseSection):
    semester: str
    schedule: str  # TODO this maybe should be like, a date time? definitely not a string.
    instructor_uris: Tuple[URIRef, ...]
    registered_student_uris: Tuple[URIRef, ...]
    course_registration_number: str
