from typing import List, Optional

from tortoise.transactions import in_transaction
from tortoise.queryset import QuerySet

from tia.mappers.projects import ProjectDTO, DevelopmentStreamDTO
from tia.models.projects import Project, DevelopmentStream


class ProjectExists(Exception):
    pass


class ProjectService:

    def _query_get_project(self, project_name: str) -> QuerySet[Project]:
        return Project.filter(name=project_name).prefetch_related('streams')

    async def get_projects(self) -> List[Project]:
        projects: List[Project] = await Project.all()
        return projects

    async def get_project(self, name: str) -> Project:
        project: Project = await self._query_get_project(name).first()
        return project

    async def add_project(self, project_dto: ProjectDTO) -> Project:
        async with in_transaction():
            count = await self._query_get_project(project_dto.name).count()
            if count:
                raise ProjectExists("Project `{project_dto.name}` already exists.")

            await Project.create(name=project_dto.name)

            project = await self._query_get_project(project_dto.name).first()
            return project

    async def add_stream(self, project_name: str, dto: DevelopmentStreamDTO) -> DevelopmentStream:
        async with in_transaction():
            project: Project = await self._query_get_project(project_name).first()
            base_stream: Optional[DevelopmentStream] = None
            stream: Optional[DevelopmentStream] = None

            for projstream in project.streams:
                if projstream.name == dto.name:
                    stream = projstream
                if projstream.name == dto.base_stream:
                    base_stream = projstream

            if not stream:
                stream = await DevelopmentStream.create(name=dto.name, project=project, base_stream=base_stream)

            return stream
