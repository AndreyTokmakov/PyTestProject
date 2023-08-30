from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../..")

from sqlalchemy import Column, Integer, String, Enum
from database.Database import Database


class TestCase(Database().base):
    __tablename__ = "TestCase"
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(256))
    path = Column(String(256))

    def __init__(self, name, description, path):
        """
        :param name: Test name
        :param description: The test case description
        :param path: Path to the test file location
        """
        self.name = name
        self.description = description
        self.path = path

    @staticmethod
    def copy_fields(src, dst):
        dst.name = src.name
        dst.description = src.description

    def __repr__(self):
        return f'TestCase(id: {self.id}, name: {self.name}, description: {self.description}, path: {self.path})'
