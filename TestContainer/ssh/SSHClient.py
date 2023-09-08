from __future__ import annotations
import socket
import time
from contextlib import ContextDecorator
from typing import Tuple

import paramiko
from scp import SCPClient


# TODO:
#   1. Connection pool
#   2. Logger
class SSHClient(object):
    SSH_PORT_DEFAULT: int = 22
    RECV_BUFFER_SIZE: int = 65535
    RECV_SOCKET_TIMEOUT: float = 0.5
    ENCODING: str = 'UTF-8'

    class ConnectionContext(ContextDecorator):

        def __init__(self, ssh_client: SSHClient) -> None:
            self.ssh_client: SSHClient = ssh_client

        def __enter__(self):
            self.ssh_client.connect()
            return self

        def __exit__(self, *exc):
            self.ssh_client.close()
            return False

    def __init__(self,
                 hostname: str,
                 username: str,
                 password: str,
                 port: int = SSH_PORT_DEFAULT):
        # self.logger = logging.getLogger("SSHClient")

        self.hostname: str = hostname
        self.username: str = username
        self.password: str = password
        self.port: int = port

        # self.status = None

        self.client: paramiko.SSHClient = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    @property
    def host(self) -> str:
        return self.hostname

    # TODO: Refactor
    def connect(self) -> None:
        self.client.connect(hostname=self.hostname,
                            username=self.username,
                            password=self.password,
                            port=self.port,
                            look_for_keys=False,
                            allow_agent=False)

    def close(self) -> None:
        self.client.close()

    # TODO: Refactor: use pool??
    #       handle possible exceptions
    def exec(self, cmd: str, timeout: int | None = None) -> Tuple[str, int]:
        with SSHClient.ConnectionContext(self):
            stdin, stdout, stderr = self.client.exec_command(command=cmd, timeout=timeout)
            data: str = (stdout.read() + stderr.read()).decode(SSHClient.ENCODING)
            return data, stdout.channel.recv_exit_status()

    def exec_shell(self, cmd: str) -> Tuple[str, int]:
        with SSHClient.ConnectionContext(self):
            output: str = ""
            exit_status: int = -1
            command: bytes = bytes(f'{cmd}\n', encoding=SSHClient.ENCODING)
            with self.client.invoke_shell() as shell:
                shell.send(command)
                shell.settimeout(self.RECV_SOCKET_TIMEOUT)

                while True:
                    try:
                        output += shell.recv(self.RECV_BUFFER_SIZE).decode(SSHClient.ENCODING)
                    except socket.timeout:
                        break
                try:
                    print('------------------ 1 -----------------------')
                    exit_status = shell.recv_exit_status()
                    print('------------------ 2 -----------------------')
                except socket.timeout:
                    pass
            return output, exit_status

    # TODO: Refactor run_executable() ???
    def run_executable(self, cmd: str, timeout: float = 60.0) -> Tuple[str, int]:
        with SSHClient.ConnectionContext(self):
            command, output = bytes(f'{cmd}\n', encoding=SSHClient.ENCODING), ""
            exit_status: int = 0
            with self.client.invoke_shell() as shell:
                shell.send(command)
                shell.settimeout(self.RECV_SOCKET_TIMEOUT)

                start: float = time.time()
                while timeout > (time.time() - start):
                    try:
                        output += shell.recv(self.RECV_BUFFER_SIZE).decode(SSHClient.ENCODING)
                    except socket.timeout:
                        break

            return output, exit_status

    def upload_file(self, src_file: str, dst_file: str) -> None:
        with SSHClient.ConnectionContext(self), SCPClient(self.client.get_transport()) as scp:
            scp.put(src_file, dst_file)
