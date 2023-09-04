import time
import warnings
from typing import List

from testcontainers.core.generic import DbContainer
from testcontainers.mysql import MySqlContainer
import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.engine import CursorResult, Engine
from sqlalchemy.orm import Query
import tables
from DatabaseDefaults import load_defaults, create_tables, add_triggers_on_changes, add_triggers_on_new_test_run
from common.TestCompletionStatus import CompletionStatus
from common.TestStatus import Status
from common.TestType import TestType
from common.TriggerType import TriggerType
from tables import TestCase
from database.Database import Database


class PyTestMySQLDatabase:
    database_container: DbContainer = None
    engine: Engine = None
    database: Database = None

    sql_version: str = 'mysql:8.1.0'
    purple_scheme: str = 'purple'

    @classmethod
    def setup_class(cls):
        cls.database_container = MySqlContainer(cls.sql_version, MYSQL_USER='root', MYSQL_PASSWORD='root',
                                                MYSQL_DATABASE='my_test').start()

        connections_string = cls.database_container.get_connection_url().replace('/my_test', '')
        cls.engine = sqlalchemy.create_engine(connections_string)
        cls.database = Database.create_database_instance(connections_string)

    @classmethod
    def teardown_class(cls):
        try:
            cls.database_container.stop()
        except Exception as exc:
            warnings.warn(message="Some problems with stopping the database container",
                          category=RuntimeWarning,
                          source=exc)
        cls.database.close()

    def test_create_database(self):
        inspector = sa.inspect(self.engine)
        assert self.purple_scheme in inspector.get_schema_names(),\
            f"Purple DB scheme {self.purple_scheme} has to be created"

    def test_create_tables(self):
        create_tables(self.database)
        tables_expected: List = ['Label', 'LabelToTestCase', 'TestCase', 'TestRun', 'TestRun2TestCase', 'TestSuite',
                                 'TestSuiteToTests', 'audit_logs', 'changes']

        result_set: CursorResult = self.database.engine.execute("SHOW TABLES;")
        tables_created: List = [entry[0] for entry in result_set]
        assert all(elem in tables_expected for elem in tables_created)

    def test_load_defaults(self):
        load_defaults(self.database)

        # TODO: Add validation
        with self.database.session as session:
            result_set: Query = session.query(tables.TestCase).order_by(TestCase.id)
            #for entry in result_set:
            #     print(entry)

    def test_triggers_on_changes_test(self):
        add_triggers_on_changes(self.database)
        tbl_name: str = 'changes'

        with self.database.session as session:
            result_set: Query = session.query(tables.AuditLogs).filter_by(table_name=tbl_name)
            assert 0 == result_set.count()

        with self.database.session as session:
            commit_data: tables.Change = tables.Change(
                committer_name="John McClane",
                committer_email="diehard@gmail.com",
                repository_url="some_repos.git",
                branch="develop",
                message="Yipee-ki-yay",
                hexsha="8556c92f96022162da21684194febfa617ead5e1",
                committed_date=1232131313,
                files_changed=str([]),
            )

            session.add(commit_data)
            session.commit()

        with self.database.session as session:
            result_set: Query = session.query(tables.AuditLogs).filter_by(table_name=tbl_name)
            assert 1 == result_set.count()

    def test_triggers_on_test_run(self):
        add_triggers_on_new_test_run(self.database)
        tbl_name: str = 'test_run'

        with self.database.session as session:
            result_set: Query = session.query(tables.AuditLogs).filter_by(table_name=tbl_name)
            assert 0 == result_set.count()

        with self.database.session as session:
            entry: tables.TestRun = tables.TestRun(type=TestType.TestSuite,
                                                   trigger=TriggerType.GitPoller,
                                                   reason=1,
                                                   status=Status.Running,
                                                   passed=CompletionStatus.Failed)
            session.add(entry)
            session.commit()

            # Simulate/force the table update operation to execute and then test the trigger
            time.sleep(0.5)
            entry.status = Status.Completed
            session.commit()

        with self.database.session as session:
            result_set: Query = session.query(tables.AuditLogs).filter_by(table_name=tbl_name)
            assert 1 == result_set.count()
