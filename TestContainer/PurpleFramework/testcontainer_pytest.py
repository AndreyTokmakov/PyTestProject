import datetime
import time

from testcontainers.core.generic import DbContainer
from testcontainers.mysql import MySqlContainer
import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.engine import CursorResult, Result, Engine
from sqlalchemy.orm import Query
import tables
from DatabaseDefaults import load_defaults, create_tables, add_triggers_on_changes, add_triggers_on_new_test_run
from common.TestCompletionStatus import CompletionStatus
from common.TestStatus import Status
from common.TestType import TestType
from common.TriggerType import TriggerType
from tables import TestCase, TestSuite, TestSuiteToTests, AuditLogs

from database.Database import Database


class DatabaseEx(Database):

    def __init__(self, conn_str: str):
        self.conn_str: str = conn_str
        super().__init__()

    @property
    def connection_string(self) -> str:
        return self.conn_str


class TestClassBlahBlahBlah:
    database: DbContainer = None
    engine: Engine = None
    connections_string: str = ""

    sql_version: str = 'mysql:8.1.0'

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which usually contains tests)."""
        print('\n', '===' * 50, '\n', '\t' * 7, 'Class SetUP\n', '===' * 50, '\n', sep='')
        cls.database = MySqlContainer(cls.sql_version, MYSQL_USER='root', MYSQL_PASSWORD='root', MYSQL_DATABASE='my_test')
        cls.database.start()

        # FIXME
        cls.connections_string = cls.database.get_connection_url().replace('/my_test', '')
        cls.engine = sqlalchemy.create_engine(cls.connections_string)

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to setup_class. """
        print('\n', '===' * 50, '\n', '\t' * 7, 'Class TeadDown\n', '===' * 50, sep='')
        try:
            cls.database.stop()
        except:  # FIXME
            print("\n\n******* OPS *******\n\n")

    def test_create_database(self):
        purple_scheme: str = 'purple'
        db = DatabaseEx(self.connections_string)
        inspector = sa.inspect(self.engine)
        assert purple_scheme in inspector.get_schema_names(), f"Purple DB scheme {purple_scheme} has to be created"

    def test_create_tables(self):
        db = DatabaseEx(self.connections_string)
        create_tables(db)

        # FIXME
        self.engine.execute(f"USE purple;")

        # TODO: Add validation
        result_set: CursorResult = self.engine.execute("SHOW TABLES;")
        for entry in result_set:
            print(entry)

    def test_load_defaults(self):
        db = DatabaseEx(self.connections_string)
        load_defaults(db)

        # TODO: Add validation
        with db.session as session:
            result_set: Query = session.query(tables.TestCase).order_by(TestCase.id)
            for entry in result_set:
                print(entry)

    def test_triggers_on_changes_test(self):
        db = DatabaseEx(self.connections_string)

        add_triggers_on_changes(db)

        with db.session as session:
            commit_data: tables.Change = tables.Change(
                committer_name="John McClane",
                committer_email="diehard@gmail.com",
                repository_url="some_repos.git",
                branch="main",
                message="commit.message",
                hexsha="commit.hexsha",
                committed_date=1232131313,
                files_changed=str([]),
            )

            session.add(commit_data)
            session.commit()

        with db.session as session:
            result_set: Query = session.query(tables.AuditLogs).filter_by(table_name='changes')
            for entry in result_set:
                print(entry)
                # TODO: Add validation
                # table_name(id: changes, timestamp: 2023-08-29 11:52:49)

    def test_triggers_on_test_run(self):
        db = DatabaseEx(self.connections_string)

        add_triggers_on_new_test_run(db)

        with db.session as session:
            entry: tables.TestRun = tables.TestRun(type=TestType.TestSuite,
                                                   trigger=TriggerType.GitPoller,
                                                   reason=1,
                                                   status=Status.Running,
                                                   passed=CompletionStatus.Failed)

            session.add(entry)
            session.commit()

            time.sleep(1)
            entry.status = Status.Completed

            session.commit()

        with db.session as session:
            result_set: Query = session.query(tables.AuditLogs).filter_by(table_name='test_run')
            for entry in result_set:
                print(entry)
                # TODO: Add validation
                # table_name(id: changes, timestamp: 2023-08-29 11:52:49)
