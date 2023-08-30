from __future__ import annotations

import time
from sqlalchemy import Column, Integer, Enum, DateTime, String
from database.Database import Database


class Change(Database().base):
    __tablename__ = "changes"
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    committer_name = Column(String(128))
    committer_email = Column(String(128))
    repository_url = Column(String(256))
    branch = Column(String(128))
    message = Column(String(1024))
    hex_sha = Column(String(64))
    committed_date = Column(Integer)
    committed_date_str = Column(String(32))
    files_changed = Column(String(2048))

    # files_changed = Column(JSON)

    def __init__(self,
                 committer_name: str,
                 committer_email: str,
                 repository_url: str,
                 branch: str,
                 message: str,
                 hexsha: str,
                 committed_date: int,
                 files_changed: str) -> None:
        """
        :param committer_name:
        :param committer_email:
        :param repository_url:
        :param branch:
        :param message:
        :param hex_sha:
        :param committed_date:
        """
        self.committer_name = committer_name
        self.committer_email = committer_email
        self.repository_url = repository_url
        self.branch = branch
        self.message = message
        self.hex_sha = hexsha
        self.committed_date = committed_date
        self.committed_date_str = time.asctime(time.gmtime(committed_date))
        self.files_changed = files_changed

    def __repr__(self):
        return f'Change(id: {self.id}, ' \
               f'committer_name: {self.committer_name}, ' \
               f'committer_email: {self.committer_email}, ' \
               f'repo: {self.repository_url}, ' \
               f'branch: {self.branch}, ' \
               f'message: {self.message}, ' \
               f'hex_sha: {self.hex_sha}, ' \
               f'committed_date: {self.committed_date_str}, ' \
               f'files_changed: {self.files_changed}' \
               ')'
