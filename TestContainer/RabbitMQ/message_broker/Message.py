
import datetime
import uuid
from typing import Dict

from pgpy import PGPKey
from pika import BasicProperties

from message_broker.PubSubParams import PubSubParams, Broker, BrokerType
from message_broker.PGPUtils import PGPUtils


class Message(object):
    UUID_PARAM: str = 'uuid'
    TIMESTAMP_PARAM: str = 'timestamp'
    TYPE_PARAM: str = 'type'

    def __init__(self) -> None:
        self.headers: Dict = {}
        self.data: bytes = None

    @property
    def broker_type(self) -> BrokerType:
        msg_type: str = self.headers.get(Message.TYPE_PARAM)
        return BrokerType[msg_type]


class MessageBuilder(object):
    key: PGPKey = PGPUtils.load_key()

    @staticmethod
    def build_message(payload: Dict, params: PubSubParams) -> Message:
        broker: Broker = params.broker
        msg: Message = Message()

        msg.headers = {
            Message.UUID_PARAM: str(uuid.uuid4()),
            Message.TIMESTAMP_PARAM: str(datetime.datetime.utcnow()),
            Message.TYPE_PARAM: broker.broker_type.name
        }

        data: str = str(payload)
        msg.data = bytes(data, encoding='utf8') if broker.is_private else PGPUtils.encrypt(MessageBuilder.key, data)
        return msg

    @staticmethod
    def extract_message(properties: BasicProperties, payload: bytes) -> Message:
        msg: Message = Message()
        msg.headers = properties.headers
        msg.data = payload.decode(encoding='utf-8') if BrokerType.Private == msg.broker_type else PGPUtils.decrypt(MessageBuilder.key, payload)
        return msg
