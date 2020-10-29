from __future__ import annotations
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from app.models import Course
from typing import FrozenSet
import math
from abc import abstractmethod


@dataclass_json
@dataclass(frozen=True)
class CourseCodeRestriction(DomainObject):
    valid_course_code_names: FrozenSet[str]
    required_special_tag_names: FrozenSet[str]
    valid_department_code_names: FrozenSet[str]
    min_level: int = 0
    max_level: int = math.inf

    def __call__(self, course: Course) -> bool:
        if course.course_code.name in self.valid_course_code_names:
            return True
        if (
            self.min_level <= course.course_code.course_level <= self.max_level
            and (
                not self.valid_department_code_names
                or course.department_code.name in self.valid_department_code_names
            )
            and all(
                tag in course.special_tags for tag in self.required_special_tag_names
            )
        ):
            return True
        return False
