from __future__ import annotations
from escore.models import Department
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject


@dataclass_json
@dataclass(frozen=True)
class Faculty(DomainObject):
    name: str
