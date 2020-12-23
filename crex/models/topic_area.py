from __future__ import annotations
from typing import Tuple
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject


@dataclass_json
@dataclass(frozen=True)
class TopicArea(DomainObject):
    name: str
    sub_topic_of: Tuple[TopicArea, ...]
    discipline: str
