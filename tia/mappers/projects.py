from __future__ import annotations
from typing import Optional, List
from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin

from tia.models.projects import Project, DevelopmentStream


@dataclass
class DevelopmentStreamDTO(DataClassJsonMixin):
    name: str
    base_stream: Optional[str] = None
    id: Optional[int] = None

    def __post_init__(self):
        # sanitize function here
        pass

    @staticmethod
    async def _from_model(model: DevelopmentStream) -> DevelopmentStreamDTO:
        base_stream = await model.base_stream if model.base_stream else None
        base_stream_name = base_stream.name if base_stream else None
        return DevelopmentStreamDTO(id=model.id, name=model.name, base_stream=base_stream_name)


@dataclass
class ProjectDTO(DataClassJsonMixin):
    name: str
    streams: List[DevelopmentStreamDTO] = field(default_factory=list)
    id: Optional[int] = None

    def __post_init__(self):
        # sanitize function here
        pass

    @staticmethod
    async def _from_model(model: Project) -> ProjectDTO:
        model_streams = await model.streams
        streams = [await DevelopmentStreamDTO._from_model(x) for x in model_streams] if model_streams else []
        return ProjectDTO(id=model.id, name=model.name, streams=streams)
