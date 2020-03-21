from quart import Quart
from tortoise.contrib.quart import register_tortoise

from tia.controllers.coverage import TestCoverageController
from tia.controllers.tests import TestController
from tia.controllers.projects import ProjectController


app = Quart(__name__)
CONNECTION_STRING = 'mysql://root:root@172.17.0.2/tia'


def register_controllers(app: Quart):
    TestCoverageController(app=app)
    TestController(app=app)
    ProjectController(app=app)


def init_database(app: Quart):
    register_tortoise(
        app,
        db_url=CONNECTION_STRING,
        modules={
            'models': [
                'tia.models.tests',
                'tia.models.projects',
                'tia.models.coverage'
            ]
        },
        generate_schemas=False
    )


init_database(app)
register_controllers(app)

if __name__ == '__main__':
    app.run(debug=True)
