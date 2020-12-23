from __future__ import annotations
from typing import Tuple
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from crex.models import DepartmentCode
from rdflib import URIRef


@dataclass_json
@dataclass(frozen=True)
class CourseCode(DomainObject):
    name: str
    cross_listed: Tuple[URIRef, ...]
    course_level: float
    department_code: DepartmentCode
