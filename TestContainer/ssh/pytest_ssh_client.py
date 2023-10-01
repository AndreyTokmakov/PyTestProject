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

        # FIXME: Solves the sometimes slow docker sshd container start-up
        time.sleep(1)

    @classmethod
    def teardown_class(cls):
        cls.sshd_container.stop()

    def test_exec_simple_command(self):
        output, code = self.client.exec(cmd='whoami')

        assert 0 == code, "Call shall succeed"
        assert self.USER_NAME in output, f'The output shall contain the username'

    def test_exec_simple_command_with_timeout(self):
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

    def test_exec_empty_command(self):
        output, code = self.client.exec(cmd='')
        assert 0 == code, "Call still shall succeed even in case if cmd is empty"

    def test_exec_long_lasting_command(self):
        count: int = 3
        start: float = time.time()
        output, code = self.client.exec(f'ping localhost -w {count}')
        duration: float = time.time() - start

        pings_send = [ln for ln in output.split('\n') if 'bytes from' in ln]

        assert 0 == code, "Call shall succeed"
        assert count == len(pings_send), f"Expecting exactly {count} lines of PING putput"
        assert count <= duration <= (count + 1), \
            f"Expected duration somewhere approximately in range {count} - {count + 1} seconds"

    def test_run_executable_with_timeout(self):
        count: int = 3  # same as timeout (one icmp is sent per one second)
        start: float = time.time()
        output, code = self.client.run_executable(cmd='ping localhost -w15', timeout=count)
        duration: float = time.time() - start

        pings_send = [ln for ln in output.split('\n') if 'bytes from' in ln]

        assert count <= len(pings_send) <= (count + 1), \
            f"Expected number of PING's somewhere approximately in range {count} - {count + 1} "
        assert count <= duration <= (count + 1), \
            f"Expected duration somewhere approximately in range {count} - {count + 1}  seconds"

    def test_run_executable_cmd_duration_over_timeout_priority(self):
        pings_count, timeout_desired = 2, 5
        start: float = time.time()
        output, code = self.client.run_executable(cmd=f'ping localhost -w {pings_count}', timeout=timeout_desired)
        duration: float = time.time() - start

        pings_send = [ln for ln in output.split('\n') if 'bytes from' in ln]

        assert pings_count <= len(pings_send) <= (pings_count + 1), \
            f"Expected number of PING's somewhere approximately in range {pings_count} - {pings_count + 1} "
        assert timeout_desired <= duration <= (timeout_desired + 1), \
            f"Expected duration somewhere approximately in range {timeout_desired} - {timeout_desired + 1}  seconds"
