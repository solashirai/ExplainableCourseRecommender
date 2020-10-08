from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject

if TYPE_CHECKING:
    from app.models import Topic, Advisor, ScheduledCourseSection


@dataclass_json
@dataclass(frozen=True)
class Student(DomainObject):
    name: str
    rin: str  # TODO: do we want to store rin?
    class_year: str
    topics_of_interest: Tuple[Topic]
    registered_courses: Tuple[ScheduledCourseSection]
    advisor: Advisor
