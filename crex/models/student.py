from __future__ import annotations
from typing import FrozenSet
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from crex.models import TopicArea, Advisor, ScheduledCourseSection, PlanOfStudy
from rdflib import URIRef


@dataclass_json
@dataclass(frozen=True)
class Student(DomainObject):
    name: str
    class_year: int
    topics_of_interest: FrozenSet[TopicArea]
    registered_courses: FrozenSet[URIRef]
    advisor: Advisor
    study_plan: PlanOfStudy
