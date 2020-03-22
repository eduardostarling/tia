from typing import Optional

from tia.controllers.base import BaseController, route
from tia.controllers.projects import STREAM_ROUTE
from tia.mappers import dtomapper
from tia.mappers.coverage import BulkCoverageDTO
from tia.services.coverage import CoverageService

COVERAGE_ROUTE = f'{STREAM_ROUTE}/coverage'
FILE_ROUTE = f'{COVERAGE_ROUTE}/file'


class TestCoverageController(BaseController):
    coverage_service: CoverageService

    def __init__(self, app, coverage_service: Optional[CoverageService] = None):
        super().__init__(app)
        self.coverage_service = coverage_service or CoverageService()

    @route(COVERAGE_ROUTE, methods=['POST'])
    @dtomapper(BulkCoverageDTO)
    async def add_results(self, project_name: str, stream_name: str, dto: BulkCoverageDTO):
        await self.coverage_service.add_results(project_name, stream_name, dto)
        return ""

    @route(f'{FILE_ROUTE}/<path:path>', methods=['GET'])
    async def get_tests_for_file(self, project_name: str, stream_name: str, path: str, hierarchy: bool = False):
        tests = await self.coverage_service.get_tests_for_file(project_name, stream_name, path, hierarchy)
        return tests.to_json()

    @route(f'{FILE_ROUTE}/hierarchy/<path:path>', methods=['GET'])
    async def get_tests_for_file_hierarchy(self, project_name: str, stream_name: str, path: str):
        return await self.get_tests_for_file(project_name, stream_name, path, hierarchy=True)
