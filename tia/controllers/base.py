from typing import Set
from functools import wraps

from quart import Quart
from sqlalchemy.orm import Session


ROUTE_ATTR = '_route'


@wraps(Quart.route)
def route(*args, **kwargs):
    def decorated(func):
        setattr(func, ROUTE_ATTR, (args, kwargs))
        return func
    return decorated


class BaseControllerMeta(type):
    def __new__(cls, name, bases, dct):
        cont: BaseController = super().__new__(cls, name, bases, dct)
        cont._routes = set()

        for attr_name, attr_value in dct.items():
            if not hasattr(attr_value, ROUTE_ATTR):
                continue
            cont._routes.add(attr_name)

        return cont


class BaseController(metaclass=BaseControllerMeta):
    _routes: Set[str]
    app: Quart
    session: Session

    def __init__(self, app: Quart, session: Session):
        self.app = app
        self.session = session
        self.__register_routes()

    def __register_routes(self):
        for route in self._routes:
            func = getattr(self, route)
            args, kwargs = getattr(func, ROUTE_ATTR)
            self.app.route(*args, **kwargs)(getattr(self, route))
