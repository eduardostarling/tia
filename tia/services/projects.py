from typing import List, Optional

from tortoise.transactions import in_transaction

from tia.mappers.projects import ProjectDTO, DevelopmentStreamDTO
from tia.models.projects import Project, DevelopmentStream
from tia.repositories.projects import ProjectRepository, DevelopmentStreamRepository


class ProjectNotFound(Exception):
    pass


class ProjectExists(Exception):
    pass


class DevStreamNotFound(Exception):
    pass


class ProjectService:
    project_repository: ProjectRepository
    devstream_repository: DevelopmentStreamRepository

    def __init__(
        self,
        project_repository: Optional[ProjectRepository] = None,
        devstream_repository: Optional[DevelopmentStreamRepository] = None
    ):
        self.project_repository = project_repository or ProjectRepository()
        self.devstream_repository = devstream_repository or DevelopmentStreamRepository()

    async def get_projects(self) -> List[Project]:
        return await self.project_repository.get_all()

    async def get_project(self, name: str) -> Project:
        project = await self.project_repository.get(name)
        if not project:
            raise ProjectNotFound()
        return project

    async def add_project(self, project_dto: ProjectDTO) -> Project:
        async with in_transaction():
            project: Optional[Project] = await self.project_repository.get(project_dto.name)
            if project:
                raise ProjectExists()

            return await self.project_repository.create(project_dto)

    async def add_stream(self, project_name: str, dto: DevelopmentStreamDTO) -> DevelopmentStream:
        async with in_transaction():
            project: Optional[Project] = await self.project_repository.get(project_name)
            if not project:
                raise ProjectNotFound()

            base_stream: Optional[DevelopmentStream] = None
            for projstream in project.streams:
                if projstream.name == dto.name:
                    return projstream

                if projstream.name == dto.base_stream:
                    base_stream = projstream

            return await self.devstream_repository.create(dev_stream_dto=dto, project=project, base_stream=base_stream)
