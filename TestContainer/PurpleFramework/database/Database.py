from __future__ import annotations
import sys, os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../..")

import sqlalchemy
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeMeta, Session
from sqlalchemy.ext.declarative import declarative_base
from common.SingletonMeta import SingletonMeta
from config.Configuration import Configuration as cfg


class Database(metaclass=SingletonMeta):
    __base__: DeclarativeMeta = declarative_base()
    __engine__: sqlalchemy.engine = None
    __db_schema__: str = 'purple'

    # TODO: do we really need that variable
    __connection_string__: str = None

    def __initialize(self, conn_str: str) -> Database:
        if not self.__engine__:
            self.__validate_scheme(conn_str)
            self.__connection_string__ = f'{conn_str}/{self.__db_schema__}'
            self.__engine__ = create_engine(url=self.__connection_string__, echo=False)

        self.__engine__.execute(f"USE {self.__db_schema__}")
        return self

    def close(self):
        self.__engine__.dispose()
        self.__engine__ = None
        self.__connection_string__ = None

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
        return self.__connection_string__

    @classmethod
    def create_database_instance(cls, conn_str: str) -> Database:
        cls.__validate_scheme(conn_str)
        return Database().__initialize(conn_str)

    @staticmethod
    def __validate_scheme(connection_string: str) -> None:
        engine = create_engine(url=connection_string)
        inspector = sa.inspect(engine)
        if Database.__db_schema__ not in inspector.get_schema_names():
            with Session(bind=engine) as session:
                session.execute(f"CREATE DATABASE {Database.__db_schema__};")
                session.commit()


# TODO: 2Discuss: not sure if its a good idea to expose/import config.Configuration here
#                 may be this module shall not be aware of Configuration at all
def create_database_default() -> Database:
    return Database.create_database_instance(
        f'mysql+pymysql://{cfg.DB_USER}:{cfg.DB_PASSWORD}@{cfg.DB_HOST}:{cfg.DB_PORT}'
    )
