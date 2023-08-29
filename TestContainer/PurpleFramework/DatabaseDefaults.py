from typing import List
import sys, os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../..")

from sqlalchemy import DDL
from database.Database import Database
from tables import TestCase, TestSuite, TestSuiteToTests, AuditLogs
from tables.Label import Label
from tables.LabelToTestCase import LabelToTestCase


def create_tables(database_instance: Database):
    database_instance.base.metadata.create_all(database_instance.engine)


def load_defaults(database_instance: Database):
    with database_instance.session as session:
        cases: List[TestCase] = []
        for idx in range(1, 11):
            cases.append(TestCase(name=f'TestCase_{idx}', description=f'Demo test case #{idx}', path='TestDemo.py'))

        cases.append(TestCase(name=f'CheckManagementFrameProtection',
                              description='Test verifies that the Management Frame Protection feature is enabled',
                              path='CheckManagementFrameProtection.py'))

        cases.append(TestCase(name=f'AuthenticationWPA3Algorithm',
                              description='Test verifies the Authentication algorithm used between two comms sleeves.\n'
                                          '1. Checks that both CSL are availalbe\n'
                                          '2. Triggers the re-Authentication procedure\n'
                                          '3. Capture the package the authentication packets and checks that algorithm == CAE',
                              path='CheckMeshAuthenticationWPA3Algorithm.py'))

        cases.append(TestCase(name=f'AuthenticationAlgorithm_DiffieHellman',
                              description='Checking that Diffie Hellman key exchange protocol is used for Authentication',
                              path='CheckMeshAuthenticationAlgorithm_DiffieHellman.py'))

        cases.append(TestCase(name=f'AuthenticationFlood',
                              description='Authentication flood test',
                              path='AuthenticationFlood.py'))

        cases.append(TestCase(name=f'AuthBombAttack',
                              description='Authentication Bomb attack test',
                              path='AuthBombAttack.py'))

        cases.append(TestCase(name=f'ArpPoisoning',
                              description='ArpPoisoning attack test',
                              path='ArpPoisoning.py'))

        labels: List[Label] = [
            Label(name=f'Regression', deletable=True),
            Label(name=f'Security', deletable=True),
            Label(name=f'Demo', deletable=True),
        ]

        suites: List[TestSuite] = [
            TestSuite(name=f'Regression Test Suite'),
            TestSuite(name=f'Security Tests'),
            TestSuite(name=f'Demo Test Suite'),
            TestSuite(name=f'Logs Test Suite'),
        ]

        suiteToTests: List[TestSuiteToTests] = [
            TestSuiteToTests(suite_id=1, test_id=1),
            TestSuiteToTests(suite_id=1, test_id=2),

            TestSuiteToTests(suite_id=2, test_id=6),
            TestSuiteToTests(suite_id=2, test_id=7),

            TestSuiteToTests(suite_id=3, test_id=11),
            TestSuiteToTests(suite_id=3, test_id=12),
            TestSuiteToTests(suite_id=3, test_id=13),
            TestSuiteToTests(suite_id=3, test_id=14),
            TestSuiteToTests(suite_id=3, test_id=15),
            TestSuiteToTests(suite_id=3, test_id=16),

            TestSuiteToTests(suite_id=4, test_id=1),
            TestSuiteToTests(suite_id=4, test_id=2),
            TestSuiteToTests(suite_id=4, test_id=3)
        ]

        label2test: List[LabelToTestCase] = [
            # Assigning the Regression label for tests:
            LabelToTestCase(labelId=1, testcaseId=11),
            LabelToTestCase(labelId=1, testcaseId=12),
            LabelToTestCase(labelId=1, testcaseId=13),
            LabelToTestCase(labelId=1, testcaseId=14),

            # Assigning the Security label for tests:
            LabelToTestCase(labelId=2, testcaseId=11),
            LabelToTestCase(labelId=2, testcaseId=12),
            LabelToTestCase(labelId=2, testcaseId=13),
            LabelToTestCase(labelId=2, testcaseId=14),
            LabelToTestCase(labelId=2, testcaseId=15),

            # Assigning the Demo label for tests:
            LabelToTestCase(labelId=3, testcaseId=1),
        ]

        session.add_all(cases)
        session.add_all(suites)
        session.add_all(labels)
        session.add_all(suiteToTests)
        session.commit()

        session.add_all(label2test)
        session.commit()


def create_triggers(database_instance: Database):
    # Create a DB trigger:
    create_on_new_changes_trigger_ddl: DDL = DDL('''\
        CREATE TRIGGER on_new_changes
            AFTER INSERT ON changes
        FOR EACH ROW
        BEGIN
            REPLACE INTO audit_logs(table_name,timestamp) VALUES ('changes', CURRENT_TIMESTAMP);
        END;''')

    create_on_test_run_trigger_ddl: DDL = DDL('''\
        CREATE TRIGGER on_new_test_run
            AFTER UPDATE ON TestRun
        FOR EACH ROW
        BEGIN
            REPLACE INTO audit_logs VALUES ('test_run', CURRENT_TIMESTAMP);
        END;''')

    database_instance.engine.execute(create_on_new_changes_trigger_ddl)
    database_instance.engine.execute(create_on_test_run_trigger_ddl)


if __name__ == '__main__':
    db: Database = Database()
    create_tables(db)
    load_defaults(db)
    create_triggers(db)

    pass
