from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../..")

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from database.Database import Database
from tables.Label import Label
from tables.TestCase import TestCase


class LabelToTestCase(Database().base):
    __tablename__ = "LabelToTestCase"
    __table_args__ = {'extend_existing': True}

    labelId = Column('labelid', Integer, ForeignKey(Label.id), primary_key=True)
    testcaseId = Column('testcaseid', Integer, ForeignKey(TestCase.id), primary_key=True)

    def __init__(self, labelId, testcaseId):
        self.labelId = labelId
        self.testcaseId = testcaseId

    def __repr__(self):
        return f'LabelToTestCase(labelId: {self.labelId}, testcaseId: {self.testcaseId})'
