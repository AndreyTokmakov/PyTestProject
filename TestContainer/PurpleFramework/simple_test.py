import time

from testcontainers.mysql import MySqlContainer
import sqlalchemy

sql_version: str = 'mysql:latest'


def create_and_check_version():
    with MySqlContainer(sql_version, MYSQL_USER='root', MYSQL_PASSWORD='root') as mysql:
        print("****************************** TEST 1 ********************************************")
        engine = sqlalchemy.create_engine(mysql.get_connection_url())
        print("****************************** TEST 2 ********************************************")

        try:
            result = engine.execute("select version()")
            version, = result.fetchone()
            print(version)
        except Exception as exc:
            print(exc)


def create_and_check_version2():
    database = MySqlContainer(sql_version, MYSQL_USER='root', MYSQL_PASSWORD='root', MYSQL_DATABASE='my_test')
    database.start()

    engine = sqlalchemy.create_engine(database.get_connection_url())
    result = engine.execute("select version()")
    print()
    print('===' * 50)
    version, = result.fetchone()
    print(version)
    print('===' * 50)

    database.stop()


if __name__ == '__main__':
    # create_and_check_version()
    create_and_check_version2()
