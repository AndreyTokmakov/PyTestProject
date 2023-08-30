from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../..")


from datetime import datetime
from sqlalchemy import Column, Integer, Enum, DateTime
from common.TestCompletionStatus import CompletionStatus
from common.TestStatus import Status
from common.TestType import TestType
from common.TriggerType import TriggerType
from database.Database import Database


class TestRun(Database().base):
    __tablename__ = "TestRun"
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    type = Column(Enum(TestType))
    trigger = Column(Enum(TriggerType))
    # reason: holds the ID of Change::id in case if trigger == GitPoller
    reason = Column(Integer)
    status = Column(Enum(Status))
    passed = Column(Enum(CompletionStatus))
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    completed_at = Column(DateTime, nullable=True)

    # TODO: Update time ??
    # updatetime = Column(TIMESTAMP(True),
    #                     nullable=False,
    #                     server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __init__(self,
                 type: TestType,
                 trigger: TriggerType,
                 reason: int,
                 status: Status,
                 passed: CompletionStatus,
                 started_at=None,
                 completed_at=None):
        """
        :param type: Type of test (security|performance|regression)
        :param trigger: Manual run|Scheduled run
        :param reason: Manual run|Scheduled run
        :param status: Enum Not started|Running|Finished
        :param passed: Enum CompletionStatus
        """
        self.type = type
        self.trigger = trigger
        self.reason = reason
        self.status = status
        self.passed = passed
        self.started_at = started_at if started_at else datetime.utcnow()
        self.completed_at = completed_at

    def __repr__(self):
        return f'id: {self.id}, status: {self.status}, passed: {self.passed}, trigger: {self.trigger}, reason: {self.reason}'
