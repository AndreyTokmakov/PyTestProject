from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/..")
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../..")
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../../..")


from datetime import datetime
from sqlalchemy import Column, String, DateTime
from database.Database import Database


class AuditLogs(Database().base):
    __tablename__ = "audit_logs"
    __table_args__ = {'extend_existing': True}

    table_name = Column(String(128), primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self,
                 table_name: str,
                 timestamp=datetime.utcnow(), ) -> None:
        """
        :param table_name:
        :param timestamp:
        """
        self.table_name = table_name
        self.timestamp = timestamp

    def __repr__(self):
        return f'table_name(id: {self.table_name}, timestamp: {self.timestamp})'
