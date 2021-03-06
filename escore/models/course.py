from __future__ import annotations
from typing import Tuple, FrozenSet
from escore.models import Department, CourseCode, TopicArea
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from rdflib import URIRef


@dataclass_json
@dataclass(frozen=True)
class Course(DomainObject):
    name: str
    description: str
    course_code: CourseCode
    special_tags: FrozenSet[
        str
    ]  # e.g. "isCommunicationIntensive". not sure if special tags is the best approach.
    required_prerequisites: FrozenSet[URIRef]
    corequisites: FrozenSet[URIRef]
    recommended_prerequisites: FrozenSet[URIRef]
    department: Department
    credits: int
    topics: FrozenSet[TopicArea]
    offering_terms: Tuple[str, ...]  # e.g. "FALL", "SPRING
    offering_period: str  # "ANNUAL", "EVEN", or "ODD"
