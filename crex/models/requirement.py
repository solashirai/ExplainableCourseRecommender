from __future__ import annotations
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from crex.models import CourseCodeRestriction
from typing import Tuple, FrozenSet
from rdflib import URIRef


@dataclass_json
@dataclass(frozen=True)
class Requirement(DomainObject):
    fulfilled_by_requirement_uris: FrozenSet[URIRef]
    sub_requirement_uris: FrozenSet[URIRef]
    restriction_requirement_uris: FrozenSet[URIRef]
    share_credits_with_requirement_uris: FrozenSet[URIRef]
    course_code_restriction: CourseCodeRestriction
    requires_credits: int = 0
