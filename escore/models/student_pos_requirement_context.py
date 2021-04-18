from __future__ import annotations
from escore.models import Student, PlanOfStudy, Requirement, Semester
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import FrozenSet


@dataclass_json
@dataclass(frozen=True)
class StudentPOSRequirementContext:
    student: Student
    plan_of_study: PlanOfStudy
    requirements: FrozenSet[Requirement]
    target_term: str = None
    target_year: int = None
