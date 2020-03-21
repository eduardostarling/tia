from typing import List, Optional
import json

from tia.controllers.base import BaseController, route
from tia.mappers import dtomapper
from tia.mappers.projects import ProjectDTO, DevelopmentStreamDTO
from tia.models.projects import Project
from tia.services.projects import ProjectService

PROJECTS_ROUTE = '/projects'
PROJECT_ROUTE = f'{PROJECTS_ROUTE}/<project_name>'
STREAMS_ROUTE = f'{PROJECT_ROUTE}/streams'
STREAM_ROUTE = f'{STREAMS_ROUTE}/<stream_name>'


class ProjectController(BaseController):
    project_service: ProjectService

    def __init__(self, app, project_service: Optional[ProjectService] = None):
        super().__init__(app)
        self.project_service = project_service or ProjectService()

    async def _from_project(self, project: Project) -> str:
        project_dto = await ProjectDTO._from_model(project)
        return project_dto.to_json()

    @route(PROJECTS_ROUTE, methods=['GET'])
    async def projects(self) -> str:
        projects: List[Project] = await self.project_service.get_projects()
        return json.dumps([x.name for x in projects])

    @route(PROJECT_ROUTE, methods=['GET'])
    async def project_details(self, project_name) -> str:
        project = await self.project_service.get_project(project_name)
        return await self._from_project(project)

    @route(PROJECTS_ROUTE, methods=['POST'])
    @dtomapper(ProjectDTO)
    async def add_project(self, dto: ProjectDTO) -> str:
        project = await self.project_service.add_project(dto)
        return await self._from_project(project)

    @route(STREAMS_ROUTE, methods=['POST'])
    @dtomapper(DevelopmentStreamDTO)
    async def add_stream(self, project_name, dto: DevelopmentStreamDTO) -> str:
        stream = await self.project_service.add_stream(project_name, dto)
        stream_dto = await DevelopmentStreamDTO._from_model(stream)
        return stream_dto.to_json()
