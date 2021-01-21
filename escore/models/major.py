from __future__ import annotations
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from escore.models import Department


@dataclass_json
@dataclass(frozen=True)
class Major(DomainObject):
    name: str
    department: Department
