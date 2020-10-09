from __future__ import annotations
from typing import Tuple
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from app.models import Instructor
from rdflib import URIRef


@dataclass_json
@dataclass(frozen=True)
class Advisor(Instructor):
    # TODO: advisors can be instructors, or they could maybe have no courses they teach. tighten up these classes.
    advises_student_uris: Tuple[URIRef]
