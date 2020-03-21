from __future__ import annotations
from typing import List
from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class BulkCoverageDTO(DataClassJsonMixin):
    results: List[TestCoverageDTO]

    def __post_init__(self):
        # sanitize function here
        pass


@dataclass
class TestCoverageDTO(DataClassJsonMixin):
    definition: str
    source_paths: List[str]


@dataclass
class FileTestsDTO(DataClassJsonMixin):
    source_path: str
    definitions: List[str]
