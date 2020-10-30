from __future__ import annotations
from crex.models import Course
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject


@dataclass_json
@dataclass(frozen=True)
class CourseSection(DomainObject):
    course: Course
    semester: str
