from __future__ import annotations
from typing import Tuple
from app.models import Department, CourseCode, Topic
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject


@dataclass_json
@dataclass(frozen=True)
class Course(DomainObject):
    name: str
    description: str
    course_code: CourseCode
    special_tags: Tuple[
        str
    ]  # e.g. "isCommunicationIntensive". not sure if special tags is the best approach.
    required_prerequisites: Tuple[Course]
    recommended_prerequisites: Tuple[Course]
    department: Department
    credits: int
    topics: Tuple[Topic]
    offered_semesters: Tuple[
        str
    ]  # e.g. "F2020". Change str to a new model later, if needed
