from __future__ import annotations
from typing import Tuple
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from app.models import Degree, CourseSection, ScheduledCourseSection, Major


@dataclass_json
@dataclass(frozen=True)
class PlanOfStudy(DomainObject):
    class_year: str
    planned_major: Major
    planned_degree: Degree
    completed_courses: Tuple[ScheduledCourseSection]
    ongoing_courses: Tuple[ScheduledCourseSection]
    planned_courses: Tuple[CourseSection]
