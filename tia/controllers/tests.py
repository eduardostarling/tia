from typing import Optional
import json

from tia.controllers.base import BaseController, route
from tia.controllers.projects import STREAM_ROUTE
from tia.mappers import dtomapper
from tia.mappers.tests import TestDefinitionDTO
from tia.services.tests import TestService

TESTS_ROUTE = f'{STREAM_ROUTE}/tests'


class TestController(BaseController):
    test_service: TestService

    def __init__(self, app, test_service: Optional[TestService] = None):
        super().__init__(app)
        self.test_service = test_service or TestService()

    @route(f'{TESTS_ROUTE}', methods=['GET'])
    async def tests(self, project_name, stream_name) -> str:
        results = await self.test_service.get_tests(project_name, stream_name)
        results_dto = {'tests': [TestDefinitionDTO._from_model(x).to_dict() for x in results]}
        return json.dumps(results_dto)

    @route(f'{TESTS_ROUTE}', methods=['POST'])
    @dtomapper(TestDefinitionDTO)
    async def add_test(self, project_name, stream_name, dto: TestDefinitionDTO):
        testdef = await self.test_service.add_test(project_name, stream_name, dto)
        return TestDefinitionDTO._from_model(testdef).to_json()
