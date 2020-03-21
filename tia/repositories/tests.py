from typing import List, Optional

from tortoise.queryset import QuerySet

from tia.mappers.tests import TestDefinitionDTO
from tia.models.projects import DevelopmentStream
from tia.models.tests import TestDefinition


class TestRepository:

    def _query_project_stream_tests(self, project_name: str, stream_name: str) -> QuerySet[TestDefinition]:
        return TestDefinition.filter(
            streams__name=stream_name,
            streams__project__name=project_name)

    async def get_all_from_stream(self, project_name: str, stream_name: str) -> List[TestDefinition]:
        return await self._query_project_stream_tests(project_name, stream_name).all()

    async def get(self, test_def_name: str, project_name: str, stream_name: str) -> Optional[TestDefinition]:
        return await self._query_project_stream_tests(project_name, stream_name).get_or_none(name=test_def_name)

    async def create(self, stream: DevelopmentStream, dto: TestDefinitionDTO) -> TestDefinition:
        testdef_add = await TestDefinition.get_or_create(name=dto.name)
        testdef = testdef_add[0]

        await testdef.streams.add(stream)

        return testdef
