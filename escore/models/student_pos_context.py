from __future__ import annotations
from escore.models import Student, PlanOfStudy
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class StudentPOSContext:
    student: Student
    plan_of_study: PlanOfStudy
