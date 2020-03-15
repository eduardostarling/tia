from typing import List

from tortoise.transactions import in_transaction
from tortoise.queryset import QuerySet

from tia.mappers.tests import TestDefinitionDTO
from tia.models.tests import TestDefinition
from tia.models.projects import DevelopmentStream


class TestExists(Exception):
    pass


class TestService:

    def _query_tests(self, project_name, stream_name) -> QuerySet[TestDefinition]:
        return TestDefinition.filter(
            streams__name=stream_name,
            streams__project__name=project_name)

    async def get_tests(self, project_name, stream_name) -> List[TestDefinition]:
        results: List[TestDefinition] = await self._query_tests(project_name, stream_name).all()
        return results

    async def add_test(self, project_name, stream_name, dto: TestDefinitionDTO) -> TestDefinition:
        async with in_transaction():
            testdef = await self._query_tests(project_name, stream_name).filter(name=dto.name)

            if not testdef:
                stream = await DevelopmentStream.filter(name=stream_name, project__name=project_name).first()
                testdef = await TestDefinition.create(name=dto.name)
                await testdef.streams.add(stream)

            return testdef
