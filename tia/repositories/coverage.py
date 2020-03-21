from typing import List

from tia.mappers.coverage import BulkCoverageDTO
from tia.models.coverage import TestCoverage, SourceCodeFile
from tia.models.projects import DevelopmentStream
from tia.models.tests import TestDefinition


class TestCoverageRepository:

    async def get_source_file(self, path: str) -> SourceCodeFile:
        source_code = await SourceCodeFile.get_or_create(path=path)
        return source_code[0]

    async def get_coverage_from_paths(self, streams: List[DevelopmentStream], paths: List[str]) -> List[TestCoverage]:
        coverage: List[TestCoverage] = []

        for path in paths:
            results = await TestCoverage.filter(stream__in=streams).all()
            coverage.extend(results)

        return coverage

    async def add_coverage(self, stream: DevelopmentStream, coverage: BulkCoverageDTO):
        for result in coverage.results:
            definition = await TestDefinition.filter(streams__id=stream.id).get(name=result.definition)

            for path_str in result.source_paths:
                source_file = await self.get_source_file(path_str)
                await TestCoverage.get_or_create(
                    definition=definition, stream=stream, source_file=source_file)

    async def get_tests_for_file(self, stream: DevelopmentStream, path: str) -> List[TestDefinition]:
        coverages = await TestCoverage.filter(
            stream=stream,
            source_file__path=path,
        ).prefetch_related('definition').all()

        definitions: List[TestDefinition] = [x.definition for x in coverages]
        return definitions

# Query for joining all tables
#
# SELECT p.name, d.name, td.name, f.path
# FROM project `p`
# INNER JOIN devstream `d` ON d.project_id=p.id
# INNER JOIN definition_stream `ds` ON ds.developmentstream_id=d.id
# INNER JOIN definition `td` ON ds.definition_id=td.id
# INNER JOIN coverage `c` ON c.stream_id=d.id AND c.definition_id=td.id
# INNER JOIN file f ON c.source_file_id=f.id;
