from typing import TypeVar, Type

from dataclasses_json import DataClassJsonMixin
from quart import request


MapType = TypeVar('MapType', bound=DataClassJsonMixin)


async def _map(type_: Type[MapType]) -> MapType:
    data = await request.get_json()
    return type_.from_dict(data)


def dtomapper(type_: Type[MapType]):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs, dto=(await _map(type_)))
        return wrapper
    return decorator
