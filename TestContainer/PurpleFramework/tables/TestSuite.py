from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../..")


from sqlalchemy import Column, Integer, String
from database.Database import Database


class TestSuite(Database().base):
    __tablename__ = "TestSuite"
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    name = Column(String(128))

    def __init__(self, name):
        """
        :param name: Test name
        """
        self.name = name

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'
