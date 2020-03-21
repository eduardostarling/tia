from __future__ import annotations
from typing import Dict, Optional
from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin

from tia.models.tests import TestDefinition


@dataclass
class TestDefinitionDTO(DataClassJsonMixin):
    name: str
    metadata: Optional[Dict[str, str]] = field(default_factory=dict)
    id: Optional[int] = None

    def __post_init__(self):
        # sanitize function here
        pass

    @staticmethod
    def _from_model(model: TestDefinition) -> TestDefinitionDTO:
        return TestDefinitionDTO(id=model.id, name=model.name)
