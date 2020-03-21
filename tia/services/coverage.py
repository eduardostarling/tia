from typing import Optional

from tia.mappers.coverage import BulkCoverageDTO, FileTestsDTO
from tia.models.projects import DevelopmentStream
from tia.repositories.coverage import TestCoverageRepository
from tia.repositories.projects import DevelopmentStreamRepository
from tia.services.projects import DevStreamNotFound


class CoverageService:
    devstream_repository: DevelopmentStreamRepository
    coverage_repository: TestCoverageRepository

    def __init__(
        self,
        devstream_repository: Optional[DevelopmentStreamRepository] = None,
        coverage_repository: Optional[TestCoverageRepository] = None
    ):
        self.devstream_repository = devstream_repository or DevelopmentStreamRepository()
        self.coverage_repository = coverage_repository or TestCoverageRepository()

    async def _get_stream(self, project_name: str, stream_name: str) -> DevelopmentStream:
        stream = await self.devstream_repository.get(stream_name, project_name)
        if not stream:
            raise DevStreamNotFound()
        return stream

    async def add_results(self, project_name: str, stream_name: str, results: BulkCoverageDTO):
        stream = await self._get_stream(project_name, stream_name)
        await self.coverage_repository.add_coverage(stream, results)

    async def get_tests_for_file(self, project_name: str, stream_name: str, path: str) -> FileTestsDTO:
        stream = await self._get_stream(project_name, stream_name)
        definitions = await self.coverage_repository.get_tests_for_file(stream, path)
        definitions_names = [x.name for x in definitions]

        return FileTestsDTO(source_path=path, definitions=definitions_names)