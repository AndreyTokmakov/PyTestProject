
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../..")

import sqlalchemy
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeMeta, Session
from sqlalchemy.ext.declarative import declarative_base
from common.SingletonMeta import SingletonMeta


class Database(metaclass=SingletonMeta):
    __base__: DeclarativeMeta = declarative_base()
    __engine__: sqlalchemy.engine = None
    DB_SCHEMA_NAME: str = 'purple'

    def __init__(self):
        if not self.connection_string:
            print('SKIPP')  # FIXME
            return

        if not self.__engine__:
            self.__engine__ = create_engine(url=f'{self.connection_string}/{self.DB_SCHEMA_NAME}',  echo=False)
            self.validate_scheme(self.connection_string)

        self.__engine__.execute(f"USE {self.DB_SCHEMA_NAME}")

    @property
    def base(self) -> DeclarativeMeta:
        return self.__base__

    @property
    def engine(self) -> sqlalchemy.engine:
        return self.__engine__

    @property
    def connection_string(self) -> str:
        # return 'mysql+pymysql://root:root@192.168.101.129:3306'
        return None

    @property
    def session(self) -> Session:
        return Session(bind=self.__engine__)

    @staticmethod
    def validate_scheme(connection_string: str) -> None:
        engine = create_engine(url=connection_string)
        inspector = sa.inspect(engine)
        if Database.DB_SCHEMA_NAME not in inspector.get_schema_names():
            with Session(bind=engine) as session:
                session.execute(f"CREATE DATABASE {Database.DB_SCHEMA_NAME};")
                session.commit()
                # print(f"CREATE DATABASE {Database.__DB_SCHEMA_NAME__} called")


