import time

from testcontainers.core.container import DockerContainer
from SSHClient import SSHClient

USER_NAME: str = 'root'
PASSWORD: str = 'root'
PORT: int = 22022


def exec_simple_command_test():
    # FIXME
    with DockerContainer("testainers/sshd-container") \
            .with_env('SSHD_USER', USER_NAME).with_env('SSHD_PASSWORD', PASSWORD) \
            .with_bind_ports(22, PORT) as container:
        time.sleep(1)

        client: SSHClient = SSHClient(hostname='0.0.0.0', username=USER_NAME, password=PASSWORD, port=PORT)
        output, code = client.exec('whoami')

        assert 0 == code, "Call shall succeed"
        assert USER_NAME in output, f'The output shall contain the username'

        # FIXME
        time.sleep(0.25)


def exec_bad_command_test():
    # FIXME
    with DockerContainer("testainers/sshd-container") \
            .with_env('SSHD_USER', USER_NAME).with_env('SSHD_PASSWORD', PASSWORD) \
            .with_bind_ports(22, PORT) as container:
        time.sleep(1)

        client: SSHClient = SSHClient(hostname='0.0.0.0', username=USER_NAME, password=PASSWORD, port=PORT)
        output, code = client.exec('some_not_existing_command_i_hope')

        assert 0 != code, "Call shall succeed"

        # FIXME
        time.sleep(0.25)


def ping_test():
    # FIXME
    with DockerContainer("testainers/sshd-container") \
            .with_env('SSHD_USER', USER_NAME).with_env('SSHD_PASSWORD', PASSWORD) \
            .with_bind_ports(22, PORT) as container:
        time.sleep(1)

        client: SSHClient = SSHClient(hostname='0.0.0.0', username=USER_NAME, password=PASSWORD, port=PORT)
        output, code = client.exec('ping localhost -w5')

        pings_send = [ln for ln in output.split('\n') if 'bytes from' in ln]

        assert 0 == code, "Call shall succeed"
        assert 5 == len(pings_send), "Expecting exactly 5 lines of PING putput"

        # FIXME
        time.sleep(0.25)


def run_executable_test():
    # FIXME
    with DockerContainer("testainers/sshd-container") \
            .with_env('SSHD_USER', USER_NAME).with_env('SSHD_PASSWORD', PASSWORD) \
            .with_bind_ports(22, PORT) as container:
        time.sleep(1)

        client: SSHClient = SSHClient(hostname='0.0.0.0', username=USER_NAME, password=PASSWORD, port=PORT)

        start: float = time.time()
        output, code = client.run_executable(cmd='ping localhost -w15', timeout=5)
        duration: float = time.time() - start

        pings_send = [ln for ln in output.split('\n') if 'bytes from' in ln]

        assert 5 <= len(pings_send) <= 7, "Expected number of PING's somewhere approximately in range 5 - 7"
        assert 5 <= duration <= 7, "Expected duration somewhere approximately in range 5 - 7 seconds"


if __name__ == '__main__':

    # exec_simple_command_test()
    exec_bad_command_test()

    # ping_test()
    # run_executable_test()
