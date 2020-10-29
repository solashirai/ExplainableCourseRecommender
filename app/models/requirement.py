from __future__ import annotations
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from app.models import CourseCodeRestriction
from typing import Tuple
from rdflib import URIRef


@dataclass_json
@dataclass(frozen=True)
class Requirement(DomainObject):
    # TODO: Requirements probably will change drastically.
    requires_credits: int
    course_code_restriction: CourseCodeRestriction
    fulfilled_by_requirement_uris: Tuple[URIRef]
    sub_requirement_uris: Tuple[URIRef]
    restriction_requirement_uris: Tuple[URIRef]
    share_credits_with_requirement_uris: Tuple[URIRef]
