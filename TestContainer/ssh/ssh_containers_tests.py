import time

from testcontainers.core.container import DockerContainer
from SSHClient import SSHClient


def start_ssh_container():
    with DockerContainer("testainers/sshd-container") \
                  .with_env('SSHD_USER', 'root').with_env('SSHD_PASSWORD', 'root') \
                  .with_bind_ports(22, 22022) as container:
        print('Started')

        client: SSHClient = SSHClient(hostname='0.0.0.0', username='root', password='root', port=22022)
        print(client.exec('ls -l'))


if __name__ == '__main__':
    start_ssh_container()
