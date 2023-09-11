import time

from testcontainers.core.container import DockerContainer
from SSHClient import SSHClient


class TestSSHClient:
    sshd_container: DockerContainer = None
    container_name: str = 'testainers/sshd-container'

    USER_NAME: str = 'root'
    PASSWORD: str = 'root'
    PORT: int = 22022

    client: SSHClient = None

    @classmethod
    def setup_class(cls):
        cls.sshd_container = DockerContainer(cls.container_name) \
            .with_env('SSHD_USER', cls.USER_NAME).with_env('SSHD_PASSWORD', cls.PASSWORD) \
            .with_bind_ports(22, cls.PORT) \
            .start()

        cls.client = SSHClient(hostname='0.0.0.0', username=cls.USER_NAME, password=cls.PASSWORD, port=cls.PORT)

    @classmethod
    def teardown_class(cls):
        cls.sshd_container.stop()

    def setup_method(self, method):
        # print('\n', '==' * 100, '\n', f'\t\tsetup_method {method}', '\n', '==' * 100, sep='')
        time.sleep(1)  # FIXME
        pass

    def teardown_method(self, method):
        # print('\n', '==' * 100, '\n', f'\t\tteardown_method {method}', '\n', '==' * 100, sep='')
        time.sleep(0.25)  # FIXME
        pass

    def test_simple_command(self):
        output, code = self.client.exec(cmd='whoami')

        assert 0 == code, "Call shall succeed"
        assert self.USER_NAME in output, f'The output shall contain the username'

    def test_simple_command_with_timeout(self):
        start: float = time.time()
        output, code = self.client.exec(cmd='whoami', timeout=5)
        duration: float = time.time() - start

        assert 0 == code, "Call shall succeed"
        assert self.USER_NAME in output, f'The output shall contain the username'
        assert 0 <= duration <= 1, "It should not take 5 seconds definitely..."

    def test_exec_bad_command(self):
        output, code = self.client.exec('some_not_existing_command_i_hope')
        assert 0 != code, "Call shall succeed"
        assert 'not found' in output

    def test_empty_command(self):
        output, code = self.client.exec(cmd='')
        assert 0 == code, "Call still shall succeed even in case if cmd is empty"

    def test_ping(self):
        output, code = self.client.exec('ping localhost -w5')

        pings_send = [ln for ln in output.split('\n') if 'bytes from' in ln]

        assert 0 == code, "Call shall succeed"
        assert 5 == len(pings_send), "Expecting exactly 5 lines of PING putput"

    def test_run_executable(self):
        start: float = time.time()
        output, code = self.client.run_executable(cmd='ping localhost -w15', timeout=5)
        duration: float = time.time() - start

        pings_send = [ln for ln in output.split('\n') if 'bytes from' in ln]

        assert 5 <= len(pings_send) <= 7, "Expected number of PING's somewhere approximately in range 5 - 7"
        assert 5 <= duration <= 7, "Expected duration somewhere approximately in range 5 - 7 seconds"
