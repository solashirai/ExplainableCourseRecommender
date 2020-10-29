from __future__ import annotations
from app.models import Course, StudentPOSRequirementContext
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import Candidate


@dataclass_json
@dataclass
class CourseCandidate(Candidate):
    domain_object: Course
    context: StudentPOSRequirementContext
