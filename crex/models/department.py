from __future__ import annotations
from typing import Tuple
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject
from rdflib import URIRef


@dataclass_json
@dataclass(frozen=True)
class Department(DomainObject):
    name: str
    offered_major_uris: Tuple[URIRef]
    offered_degree_uris: Tuple[URIRef]
