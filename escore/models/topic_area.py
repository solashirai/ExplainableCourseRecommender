from __future__ import annotations
from typing import FrozenSet
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import DomainObject


@dataclass_json
@dataclass(frozen=True)
class TopicArea(DomainObject):
    name: str
    sub_topic_of: FrozenSet[TopicArea]
    discipline: str
