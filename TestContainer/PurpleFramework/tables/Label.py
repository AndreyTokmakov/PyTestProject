from __future__ import annotations
from sqlalchemy import Column, Integer, String, Boolean
from database.Database import Database


class Label(Database().base):
    __tablename__ = "Label"
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    name = Column("name", String(100))
    deletable = Column("deletable", Boolean)

    def __init__(self, name, deletable):
        self.name = name
        self.deletable = deletable

    def __repr__(self):
        return f'Label(id: {self.id}, name: {self.name}, deletable: {self.deletable})'
