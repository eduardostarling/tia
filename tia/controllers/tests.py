import json

from tortoise.transactions import in_transaction
from tortoise.queryset import QuerySet

from tia.controllers.base import BaseController, route
from tia.mappers import dtomapper
from tia.mappers.tests import TestDefinitionDTO
from tia.models.tests import TestDefinition
from tia.models.projects import DevelopmentStream


BASE_ROUTE = '/projects/<project_name>/streams/<stream_name>'


class TestController(BaseController):

    def _query_tests(self, project_name, stream_name) -> QuerySet[TestDefinition]:
        return TestDefinition.filter(
            streams__name=stream_name,
            streams__project__name=project_name)

    @route(f"{BASE_ROUTE}/tests", methods=['GET'])
    async def tests(self, project_name, stream_name) -> str:
        results = await self._query_tests(project_name, stream_name).all()
        results_dto = [TestDefinitionDTO._from_model(x).to_dict() for x in results]

        return json.dumps(results_dto)

    @route(f"{BASE_ROUTE}/tests", methods=['POST'])
    @dtomapper(TestDefinitionDTO)
    async def add_test(self, project_name, stream_name, dto: TestDefinitionDTO):
        async with in_transaction():
            count = await self._query_tests(project_name, stream_name).filter(name=dto.name).count()
            if count:
                return "Already exists"

            stream = await DevelopmentStream.filter(name=stream_name, project__name=project_name).first()
            testdef = await TestDefinition.create(name=dto.name)
            await testdef.streams.add(stream)

        return TestDefinitionDTO._from_model(testdef).to_json(), 200
