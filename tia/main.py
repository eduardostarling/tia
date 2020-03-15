from typing import Tuple
import asyncio

from quart import Quart
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_aio import ASYNCIO_STRATEGY
from sqlalchemy_aio.engine import AsyncioEngine

from tia.models.base import Base
from tia.controllers.tests import TestController

CONNECTION_STRING = 'mysql+pymysql://root:root@172.17.0.2/tia'


def register_controllers(app: Quart, session: Session):
    TestController(app=app, session=session)


async def get_database_engine(migrate=False) -> Tuple[AsyncioEngine, Session]:
    engine: AsyncioEngine = create_engine(CONNECTION_STRING, strategy=ASYNCIO_STRATEGY)

    if migrate:
        await engine.run_in_thread(Base.metadata.create_all, engine.sync_engine)

    await engine.connect()  # type: ignore
    session = sessionmaker(bind=engine)
    return engine, session()


async def main():
    db_engine, session = await get_database_engine(migrate=True)

    app = Quart(__name__)
    register_controllers(app, session)

    try:
        await app.run_task()
    finally:
        await db_engine.close()

if __name__ == "__main__":
    asyncio.run(main(), debug=True)
