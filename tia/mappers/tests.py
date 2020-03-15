from __future__ import annotations
from typing import Optional
from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin

from tia.models.tests import TestDefinition


@dataclass
class TestDefinitionDTO(DataClassJsonMixin):
    name: str
    id: Optional[int] = None

    def __post_init__(self):
        # sanitize function here
        pass

    @staticmethod
    def _from_model(model: TestDefinition) -> TestDefinitionDTO:
        return TestDefinitionDTO(id=model.id, name=model.name)
