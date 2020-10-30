from __future__ import annotations
from typing import Tuple
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from crex.models import Faculty
from rdflib import URIRef


@dataclass_json
@dataclass(frozen=True)
class Instructor(Faculty):
    teaches_scheduled_course_uris: Tuple[URIRef]
