from typing import List, Optional

from tortoise.queryset import QuerySet

from tia.mappers.projects import ProjectDTO, DevelopmentStreamDTO
from tia.models.projects import Project, DevelopmentStream


class ProjectRepository:

    def _query_project(self, project_name: str) -> QuerySet[Project]:
        return Project.filter(name=project_name).prefetch_related('streams')

    async def get_all(self) -> List[Project]:
        projects: List[Project] = await Project.all()
        return projects

    async def get(self, project_name: str) -> Optional[Project]:
        return await self._query_project(project_name).get_or_none()

    async def create(self, project_dto: ProjectDTO) -> Project:
        return await Project.create(name=project_dto.name)


class DevelopmentStreamRepository:

    def _query_stream(self, stream_name: str, project_name: str) -> QuerySet[DevelopmentStream]:
        return DevelopmentStream.filter(name=stream_name, project__name=project_name)

    async def get(self, stream_name: str, project_name: str) -> Optional[DevelopmentStream]:
        return await self._query_stream(stream_name, project_name).get_or_none()

    async def get_ordered_hierarchy(self, stream_name: str, project_name: str) -> List[DevelopmentStream]:
        all_streams = await DevelopmentStream.filter(project__name=project_name).prefetch_related('base_stream').all()
        streams = []

        def seek_stream(name: str):
            stream: DevelopmentStream

            for stream in all_streams:
                if stream.name == stream_name:
                    streams.append(stream)
                    if stream.base_stream:
                        seek_stream(stream.base_stream.name)
                    break

        return streams

    async def create(
        self, dev_stream_dto: DevelopmentStreamDTO, project: Project, base_stream: Optional[DevelopmentStream]
    ) -> DevelopmentStream:

        return await DevelopmentStream.create(name=dev_stream_dto.name, project=project, base_stream=base_stream)
