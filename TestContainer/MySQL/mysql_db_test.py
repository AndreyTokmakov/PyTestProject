from testcontainers.mysql import MySqlContainer
import sqlalchemy
import sqlalchemy as sa
from sqlalchemy.engine import CursorResult, Result, Engine
from Database import Database
from TestContainer.PurpleFramework import tables
from TestContainer.PurpleFramework.database.Database import Database
from TestContainer.PurpleFramework.tables import TestCase, TestSuite, TestSuiteToTests, AuditLogs

sql_version: str = 'mysql:8.1.0'


def create_and_check_version():
    with MySqlContainer(sql_version, MYSQL_USER='root', MYSQL_PASSWORD='root') as mysql:
        engine = sqlalchemy.create_engine(mysql.get_connection_url())
        result = engine.execute("select version()")
        version, = result.fetchone()
        print(version)


def create_database():
    with MySqlContainer(sql_version, MYSQL_USER='root', MYSQL_PASSWORD='root') as mysql:
        engine: Engine = sqlalchemy.create_engine(mysql.get_connection_url())

        databases = engine.execute("SHOW DATABASES;")
        for db in databases:
            print(db)
        print('=='*70)

        result = engine.execute(f"CREATE DATABASE purple;")

        databases = engine.execute("SHOW DATABASES;")
        for db in databases:
            print(db)


def create_database_test_creation():
    with MySqlContainer(sql_version, MYSQL_USER='root', MYSQL_PASSWORD='root') as mysql:
        engine: Engine = sqlalchemy.create_engine(mysql.get_connection_url())
        Database.create_scheme(mysql.get_connection_url())
    
        inspector = sa.inspect(engine)
        assert 'purple' in inspector.get_schema_names(), "Purple DB scheme has to be created"



'''
Database
'''


# Check create DB
# Check tables creation
# Check triggers
# Check for MySQL and MarinaDB
if __name__ == '__main__':
    # create_database()
    create_database_test_creation()
    # create_and_check_version()
