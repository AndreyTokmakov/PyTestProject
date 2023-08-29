from __future__ import annotations

import sqlalchemy
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeMeta, Session
from sqlalchemy.ext.declarative import declarative_base

from SingletonMeta import SingletonMeta


class Database(metaclass=SingletonMeta):
    __base__: DeclarativeMeta = declarative_base()
    __engine__: sqlalchemy.engine = None

    __DB_SCHEMA_NAME__: str = 'purple'

    def __init__(self, connection_string: str) -> None:
        self.__CONNECT_STRING__ = connection_string
        if not self.__engine__:
            self.__engine__ = create_engine(url=f'{self.__CONNECT_STRING__}/{self.__DB_SCHEMA_NAME__}',
                                            echo=False)
            self.__engine__.execute(f"USE {self.__DB_SCHEMA_NAME__}")

    @property
    def base(self) -> DeclarativeMeta:
        return self.__base__

    @property
    def engine(self) -> sqlalchemy.engine:
        return self.__engine__

    @property
    def session(self) -> Session:
        return Session(bind=self.__engine__)

    @property
    def connection_string(self) -> str:
        return f'{self.__CONNECT_STRING__}/{self.__DB_SCHEMA_NAME__}'

    @staticmethod
    def create_scheme(connection_string: str) -> None:
        engine = create_engine(url=connection_string)
        inspector = sa.inspect(engine)
        if Database.__DB_SCHEMA_NAME__ not in inspector.get_schema_names():
            with Session(bind=engine) as session:
                session.execute(f"CREATE DATABASE {Database.__DB_SCHEMA_NAME__};")
                session.commit()


# Do we need to protect it with Mutex / Lock
# Database.create_scheme()

# database_instance: Database = Database()
