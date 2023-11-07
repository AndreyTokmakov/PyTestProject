import enum
import pika

from pika.connection import Parameters, SSLOptions
from pika.exchange_type import ExchangeType


class BrokerType(enum.Enum):
    Private = 0
    Public = 1
    All = 2


class Broker(object):

    def __init__(self,
                 host: str,
                 username: str,
                 password: str,
                 port: int = Parameters.DEFAULT_PORT,
                 ssl_options: SSLOptions = Parameters.DEFAULT_SSL_OPTIONS,
                 broker_type: BrokerType = BrokerType.Private) -> None:
        self.host: str = host
        self.port: int = port
        self.credentials = pika.PlainCredentials(username, password)
        self.ssl_options: SSLOptions = ssl_options
        self.broker_type: BrokerType = broker_type

    @property
    def is_public(self) -> bool:
        return self.broker_type == BrokerType.Public

    @property
    def is_private(self) -> bool:
        return self.broker_type == BrokerType.Private


class Routing(object):

    def __init__(self,
                 exchange: str,
                 topic: str,
                 durable: bool = True,
                 exchange_type: ExchangeType = ExchangeType.topic,
                 virtual_host: str = Parameters.DEFAULT_VIRTUAL_HOST) -> None:
        self.exchange: str = exchange
        self.topic: str = topic
        self.virtual_host: str = virtual_host
        self.exchange_type: ExchangeType = exchange_type
        self.durable: bool = durable


class PubSubParams(object):

    def __init__(self,
                 broker: Broker,
                 routing: Routing) -> None:
        self.broker: Broker = broker
        self.routing: Routing = routing
