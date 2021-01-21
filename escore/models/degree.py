from __future__ import annotations
from rdflib import URIRef
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from typing import Tuple
from escore.models import Major, Department, Requirement


@dataclass_json
@dataclass(frozen=True)
class Degree(DomainObject):
    name: str
    major: Major  # currently assuming 1 major
    requirements: Tuple[Requirement, ...]
