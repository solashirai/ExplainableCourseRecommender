from __future__ import annotations
from crex.models import Student, PlanOfStudy, Requirement
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import FrozenSet


@dataclass_json
@dataclass(frozen=True)
class StudentPOSRequirementContext:
    student: Student
    plan_of_study: PlanOfStudy
    requirements: FrozenSet[Requirement]
