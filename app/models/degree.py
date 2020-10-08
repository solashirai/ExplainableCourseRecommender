from __future__ import annotations
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Major, Department


@dataclass_json
@dataclass(frozen=True)
class Degree(DomainObject):
    name: str
    description: str
    major: Major  # currently assuming 1 major
    department: Department
