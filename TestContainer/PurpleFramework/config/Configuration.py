import enum
import os
from pathlib import Path
from typing import List

from common.SingletonMeta import SingletonMeta


class NodeType(enum.Enum):
    CommsSleeve = 0
    Agent = 1
    Switch = 2
    Other = 3

    def __str__(self):
        return str(self.name)


class Node(object):

    def __init__(self,
                 name: str = "",
                 host: str = "",
                 user_name: str = "",
                 password: str = "",
                 node_tpe: NodeType = NodeType.Other):
        self.name: str = name
        self.host: str = host
        self.user_name: str = user_name
        self.password: str = password
        self.type: NodeType = node_tpe


# TODO:
#  1. Agent
#     - inject  WiFi interface | Name, IP, Mac
#     - monitor WiFi interface | Name, IP, Mac
# TODO:
#  2. CommsSleeve
#     - AP   WiFi interface | Name, IP, Mac
#     - Mesh WiFi interface | Name, IP, Mac


class Configuration(metaclass=SingletonMeta):
    PROJECT_ROOT_DIR: Path = Path(os.path.realpath(__file__)).parent.parent
    TESTS_DIR: Path = PROJECT_ROOT_DIR.joinpath('tests')
    CONFIG_DIR: Path = PROJECT_ROOT_DIR.joinpath('config')

    # Database (MySQL):
    DB_HOST: str = '192.168.101.2'
    DB_PORT: int = 3306
    DB_USER: str = 'root'
    DB_PASSWORD: str = 'root'

    nodes: List[Node] = [
        Node('CommsSleeve1', '192.168.101.101', 'root', 'root', NodeType.CommsSleeve),
        Node('CommsSleeve2', '192.168.101.102', 'root', 'root', NodeType.CommsSleeve),
        Node('Laptop', '192.168.101.102', 'root', 'root', NodeType.CommsSleeve),
    ]

    PY_INTERPRETER: str = '/home/andtokm/Projects/PythonVenvs/venv/bin/python'

    AGENT_HOST: str = '192.168.101.1'

    AGENT_WIFI_IFACE: str = 'wlp0s20f3'
    # AGENT_WIFI_IFACE_MAC: str = 'BC:6E:E2:03:74:BA'  # Laptop1
    AGENT_WIFI_IFACE_MAC: str = '38:7A:0E:2A:77:CC'  # Laptop2
    AGENT_MONITOR_IFACE: str = 'wlx00c0cab21ffc'

    USER_NAME: str = 'andtokm'
    ROOT_USER: str = 'root'
    PASSWORD: str = '123!@#QWEqwe'

    CSL_HOST_1: str = '192.168.101.101'
    CSL_HOST_2: str = '192.168.101.102'

    CSL_USER: str = 'root'
    CSL_PASSWORD: str = 'root'

    CSL_WIFI_AP_NAME: str = 'comms_sleeve#5bfc'
    CSL_WIFI_INTERFACE: str = 'wlan1'
    CSL_WIFI_MAC_ADDRESS: str = 'E4:5F:01:61:5B:FC'
    CSL_WIFI_AP_PASSWORD: str = 'ssrcdemo'

    CSL1_MESH_MAC: str = '00:30:1a:4f:8d:c4'
    CSL2_MESH_MAC: str = '00:30:1a:4e:fa:53'

    # MONGO_DB_CONNECTION_STRING: str = "mongodb://admin:admin@0.0.0.0/"
    MONGO_DB_CONNECTION_STRING: str = "mongodb://admin:admin@192.168.101.2/"

    API_TESTS_READY_URL: str = "http://0.0.0.0:5005/api/testsready"

    def __init__(self):
        pass

    # TODO: Refactor
    def __repr__(self):
        return f'Configuration()'
