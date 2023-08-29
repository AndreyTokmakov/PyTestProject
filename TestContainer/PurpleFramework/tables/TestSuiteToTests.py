from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../..")

from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from database.Database import Database


class TestSuiteToTests(Database().base):
    __tablename__ = "TestSuiteToTests"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    suite_id = Column(Integer, primary_key=False, nullable=False)
    test_id = Column(Integer, primary_key=False, nullable=False)

    # TODO: We need to make suite_id and  test_id a ForeignKey's
    '''
    suite_id = Column(Integer,
                      ForeignKey('TestSuite.id', ondelete='CASCADE'), 
                      nullable=False)
    test_id = Column(Integer,
                     ForeignKey('TestCase.id', ondelete='CASCADE'),
                     nullable=False)
    '''

    def __init__(self, suite_id: int, test_id: int):
        """
        :param suite_id: Test Suite ID
        :param test_id : Test case ID
        """
        self.suite_id = suite_id
        self.test_id = test_id

    def __repr__(self):
        return f'id: {self.id}, suite_id: {self.suite_id}, test_id: {self.test_id}'
