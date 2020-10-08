from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from app.models import Faculty

if TYPE_CHECKING:
    from app.models import ScheduledCourseSection


@dataclass_json
@dataclass(frozen=True)
class Instructor(Faculty):
    teaches_courses: Tuple[ScheduledCourseSection]
