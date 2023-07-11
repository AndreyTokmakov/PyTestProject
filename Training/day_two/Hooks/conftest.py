import sys

import pytest
import datetime
from pathlib import Path
from _pytest.main import Session
from _pytest.nodes import Item
from _pytest.runner import CallInfo
from _pytest.terminal import TerminalReporter
from _pytest.tmpdir import tmp_path
from pytest import Config

# failed_test_file = Path() / 'failures.txt'
failed_test_file = Path('/tmp/pytest-of-andtokm/failures.txt')


@pytest.hookimpl()
def pytest_sessionstart(session: Session):
    print(f'Starting session: {datetime.datetime.now()}, tmp: {failed_test_file}')

    if failed_test_file.exists():
        print(f'File {failed_test_file} exists. Recreating it')
        failed_test_file.unlink()
        failed_test_file.touch()
    else:
        print(f'File {failed_test_file} do not exists')


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: CallInfo):
    out = yield
    results = out.get_result()
    if results.when == 'call' and results.failed:
        try:
            with open(str(failed_test_file), 'a') as file:
                file.write(results.nodeid + '\n')
        except Exception as exc:
            print(f"Error: {exc}")
            pass


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter: TerminalReporter,
                            exitstatus: int,
                            config: Config):
    yield
    print(f'For more details run: car {failed_test_file}')
