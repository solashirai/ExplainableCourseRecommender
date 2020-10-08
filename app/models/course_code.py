from __future__ import annotations
from typing import Tuple
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject


@dataclass_json
@dataclass(frozen=True)
class CourseCode(DomainObject):
    name: str
    cross_listed: Tuple[CourseCode]
    course_level: int
