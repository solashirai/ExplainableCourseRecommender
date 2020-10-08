from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject

if TYPE_CHECKING:
    from app.models import Major, Degree


@dataclass_json
@dataclass(frozen=True)
class Department(DomainObject):
    name: str
    offered_majors: Tuple[Major]
    offered_degrees: Tuple[Degree]
