from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../..")

from datetime import datetime
from sqlalchemy import Column, Integer, Enum, DateTime
from common.TestCompletionStatus import CompletionStatus
from database.Database import Database


class TestRun2TestCase(Database().base):
    # TODO: Rname to snake_case ???
    __tablename__ = "TestRun2TestCase"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)

    run_id = Column(Integer, primary_key=False, nullable=False)
    test_id = Column(Integer, primary_key=False, nullable=False)
    passed = Column(Enum(CompletionStatus))
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    completed_at = Column(DateTime, nullable=True)

    '''
    # TODO: We need to make run_id and test_id a ForeignKey's
    run_id = Column(Integer,
                    ForeignKey('TestRun.id', ondelete='CASCADE'),
                    nullable=False)
    test_id = Column(Integer,
                     ForeignKey('TestCase.id', ondelete='CASCADE'),
                     nullable=False)
    '''

    def __init__(self,
                 run_id,
                 test_id,
                 passed,
                 started_at=None,
                 completed_at=None) -> None:
        """
        :param run_id  : Test Run ID
        :param test_id : Test case ID
        """
        self.run_id = run_id
        self.test_id = test_id
        self.passed = passed
        self.started_at = started_at if started_at else datetime.utcnow()
        self.completed_at = completed_at

    def __repr__(self):
        return f'id: {self.id}, suite_id: {self.run_id}, test_id: {self.test_id}, passed: {self.passed}'
