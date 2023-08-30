from sqlalchemy.orm import Query

from TestContainer.PurpleFramework import tables
from TestContainer.PurpleFramework.database.Database import Database
from TestContainer.PurpleFramework.tables import TestCase, TestSuite, TestSuiteToTests, AuditLogs


class DatabaseEx(Database):

    def __init__(self, conn_str: str):
        self.conn_str: str = conn_str
        super().__init__()

    @property
    def connection_string(self) -> str:
        return self.conn_str


database_instance = DatabaseEx('mysql+pymysql://root:root@192.168.101.2:3306')


def select_test_cases():
    with database_instance.session as session:
        result_set: Query = session.query(tables.TestCase).order_by(TestCase.id)
        for entry in result_set:
            print(entry)


def select_test_suites():
    with database_instance.session as session:
        result_set: Query = session.query(tables.TestSuite).order_by(TestSuite.id)
        for entry in result_set:
            print(entry)


def select_labels():
    with database_instance.session as session:
        result_set: Query = session.query(tables.Label).order_by(tables.Label.id)
        for entry in result_set:
            print(entry)


def select_test_runs():
    with database_instance.session as session:
        result_set: Query = session.query(tables.TestRun).order_by(tables.TestRun.id)
        for entry in result_set:
            print(entry)


def select_test_runs_2_test_case():
    with database_instance.session as session:
        result_set: Query = session.query(tables.TestRun2TestCase).order_by(tables.TestRun2TestCase.id)
        for entry in result_set:
            print(entry)


#
def select_changes():
    with database_instance.session as session:
        result_set: Query = session.query(tables.Change).order_by(tables.Change.id)
        for entry in result_set:
            print(entry)


def select_suite_2_tests():
    with database_instance.session as session:
        result_set: Query = session.query(tables.TestSuiteToTests).order_by(tables.TestSuiteToTests.id)
        for entry in result_set:
            print(entry)


def select_label_2_tests():
    with database_instance.session as session:
        result_set: Query = session.query(tables.LabelToTestCase).order_by(tables.LabelToTestCase.labelId)
        for entry in result_set:
            print(entry)


def select_audit_logs():
    with database_instance.session as session:
        result_set: Query = session.query(tables.AuditLogs)
        for entry in result_set:
            print(entry)


if __name__ == '__main__':
    select_test_cases()
    # select_test_suites()
    # select_labels()
    # select_test_runs()
    # select_test_runs_2_test_case()
    # select_audit_logs()
    # select_changes()
    # select_suite_2_tests()

    pass
