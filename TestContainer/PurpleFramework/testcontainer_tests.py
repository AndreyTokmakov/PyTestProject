import datetime
import time

from testcontainers.mysql import MySqlContainer
import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.engine import CursorResult, Result, Engine
from sqlalchemy.orm import Query
import tables
from DatabaseDefaults import load_defaults, create_tables, create_triggers
from tables import TestCase, TestSuite, TestSuiteToTests, AuditLogs

from database.Database import Database


class DatabaseEx(Database):

    def __init__(self, conn_str: str):
        self.conn_str: str = conn_str
        super().__init__()

    @property
    def connection_string(self) -> str:
        return self.conn_str


sql_version: str = 'mysql:8.1.0'


def create_and_check_version():
    with MySqlContainer(sql_version, MYSQL_USER='root', MYSQL_PASSWORD='root') as mysql:
        engine = sqlalchemy.create_engine(mysql.get_connection_url())
        result = engine.execute("select version()")
        version, = result.fetchone()
        print(version)


def create_database_test_creation():
    purple_scheme: str = 'purple'
    with MySqlContainer(sql_version, MYSQL_USER='root', MYSQL_PASSWORD='root', MYSQL_DATABASE='my_test') as mysql:
        # FIXME: Dirty hack
        conn_str: str = mysql.get_connection_url().replace('/my_test', '')
        database_instance = DatabaseEx(conn_str)
        inspector = sa.inspect(database_instance.engine)
        assert purple_scheme in inspector.get_schema_names(), f"Purple DB scheme {purple_scheme} has to be created"


def create_table_test():
    with MySqlContainer(sql_version, MYSQL_USER='root', MYSQL_PASSWORD='root', MYSQL_DATABASE='my_test') as mysql:
        # FIXME: Dirty hack
        conn_str: str = mysql.get_connection_url().replace('/my_test', '')
        db = DatabaseEx(conn_str)
        print(f'************ {conn_str} ***************')

        create_tables(db)
        db = DatabaseEx(None)


def load_default_values_test():
    with MySqlContainer(sql_version, MYSQL_USER='root', MYSQL_PASSWORD='root', MYSQL_DATABASE='my_test') as mysql:
        # FIXME: Dirty hack
        conn_str: str = mysql.get_connection_url().replace('/my_test', '')
        db = DatabaseEx(conn_str)
        print(f'************ {conn_str} ***************')

        create_tables(db)
        load_defaults(db)

        with db.session as session:
            result_set: Query = session.query(tables.TestCase).order_by(TestCase.id)
            for entry in result_set:
                print(entry)


def test_triggers_on_changes_test():
    with MySqlContainer(sql_version, MYSQL_USER='root', MYSQL_PASSWORD='root', MYSQL_DATABASE='my_test') as mysql:
        # FIXME: Dirty hack
        conn_str: str = mysql.get_connection_url().replace('/my_test', '')
        db = DatabaseEx(conn_str)

        create_tables(db)
        create_triggers(db)

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
                # table_name(id: changes, timestamp: 2023-08-29 11:52:49)


def select_test_cases():
    database_instance = DatabaseEx('mysql+pymysql://root:root@192.168.101.2:3306')
    with database_instance.session as session:
        result_set: Query = session.query(tables.TestCase).order_by(TestCase.id)
        for entry in result_set:
            print(entry)


# load_defaults
# Check create DB
# Check tables creation
# Check triggers
# Check for MySQL and MarinaDB
# Load defaults
if __name__ == '__main__':
    # create_database()
    # create_database_test_creation()
    # create_and_check_version()

    # create_table_test()
    # load_default_values_test()
    test_triggers_on_changes_test()

    # select_test_cases()
