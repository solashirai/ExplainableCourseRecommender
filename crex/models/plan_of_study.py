from __future__ import annotations
from typing import Tuple, FrozenSet
from rdflib import URIRef
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from crex.models import Degree, Major


@dataclass_json
@dataclass(frozen=True)
class PlanOfStudy(DomainObject):
    class_year: str
    planned_major: Major
    planned_degree: Degree
    completed_course_sections: FrozenSet[URIRef]
    ongoing_course_sections: FrozenSet[URIRef]
    planned_course_sections: FrozenSet[URIRef]
