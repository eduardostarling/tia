from quart import request

from tia.controllers.base import BaseController, route
from tia.models.tests import TestDefinition, TestResult, Project, DevelopmentStream


class TestController(BaseController):

    @route("/get-tests", methods=['GET'])
    async def tests(self) -> str:
        query = self.session.query(TestDefinition)
        results = await self.session.execute(query)
        return str(results)

    @route("/add-test", methods=['POST'])
    async def add_test(self):
        data = await request.get_json()
        name = data["name"]

        query = await self.session.query(TestDefinition).filter(TestDefinition.name == name)

        if query.all():
            return "Already exists"

        self.session.begin()
        tdef = TestDefinition(name=data["name"])
        self.session.add(tdef)
        self.session.commit()
