from typing import List, Optional

from tortoise.transactions import in_transaction

from tia.mappers.tests import TestDefinitionDTO
from tia.models.tests import TestDefinition
from tia.repositories.projects import DevelopmentStreamRepository
from tia.repositories.tests import TestRepository


class TestExists(Exception):
    pass


class DevStreamNotFound(Exception):
    pass


class TestService:
    test_repository: TestRepository
    devstream_repository: DevelopmentStreamRepository

    def __init__(
        self,
        test_respository: Optional[TestRepository] = None,
        devstream_repository: Optional[DevelopmentStreamRepository] = None
    ):
        self.test_repository = test_respository or TestRepository()
        self.devstream_repository = devstream_repository or DevelopmentStreamRepository()

    async def get_tests(self, project_name: str, stream_name: str) -> List[TestDefinition]:
        return await self.test_repository.get_all_from_stream(project_name, stream_name)

    async def add_test(self, project_name: str, stream_name: str, dto: TestDefinitionDTO) -> TestDefinition:
        async with in_transaction():
            stream = await self.devstream_repository.get(stream_name, project_name)
            if not stream:
                raise DevStreamNotFound()

            testdef = await self.test_repository.get(dto.name, project_name, stream_name)
            if not testdef:
                testdef = await self.test_repository.create(stream, dto)

            return testdef
