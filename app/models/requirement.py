from __future__ import annotations
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from typing import Tuple
from rdflib import URIRef


@dataclass_json
@dataclass(frozen=True)
class Requirement(DomainObject):
    # TODO: Requirements probably will change drastically.
    required_credits: int
    valid_course_uris: Tuple[URIRef]
    fulfilled_by_requirement_uris: Tuple[URIRef]
