from __future__ import annotations
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from crex.models import Course
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
        elif (
            not self.valid_course_code_names  # if the restriction checks for exact names, return false past here
            and self.min_level
            <= course.course_code.course_level
            <= self.max_level  # check course level
            and (
                not self.valid_department_code_names  # if no department codes are specified, assume any are fine
                or course.course_code.department_code.name
                in self.valid_department_code_names
            )
            and all(  # for special tag restrictions, valid courses should have all required tags
                tag in course.special_tags for tag in self.required_special_tag_names
            )
        ):
            return True
        return False
