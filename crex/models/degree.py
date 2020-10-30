from __future__ import annotations
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from typing import Tuple
from crex.models import Major, Department, Requirement


@dataclass_json
@dataclass(frozen=True)
class Degree(DomainObject):
    name: str
    description: str
    major: Major  # currently assuming 1 major
    department: Department
    requirements: Tuple[Requirement]
