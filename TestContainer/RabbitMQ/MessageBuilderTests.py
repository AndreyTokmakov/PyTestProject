import sys, os
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "..")
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../..")
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../../..")

import pytest

from pika import BasicProperties
from typing import List, Dict
from testcontainers.rabbitmq import RabbitMqContainer
from message_broker.Consumer_Thread_Queue import MessageBus
from message_broker.PubSubParams import Routing, Broker, PubSubParams, BrokerType
from message_broker.Message import Message, MessageBuilder


def test_build_message_payload_plaint():
    message: Dict = {'username': 'root', 'password': 'qwerty'}
    params = PubSubParams(Broker('', '', '', broker_type=BrokerType.Private), None)

    msg: Message = MessageBuilder.build_message(message, params)
    assert msg.headers
    assert msg.data

    payload = msg.data.decode(encoding='utf-8')
    assert str(message) in payload


def test_build_message_payload_encrypted():
    message: Dict = {'username': 'root', 'password': 'qwerty'}
    params = PubSubParams(Broker('', '', '', broker_type=BrokerType.Public), None)

    msg: Message = MessageBuilder.build_message(message, params)
    assert msg.headers
    assert msg.data

    # We shall fail to decode the message
    with pytest.raises(UnicodeDecodeError):
        payload = msg.data.decode(encoding='utf-8')


@pytest.mark.parametrize("broker_type", [BrokerType.Private, BrokerType.Public])
def test_build_message_header(broker_type):
    message: Dict = {'username': 'root', 'password': 'qwerty'}
    params = PubSubParams(Broker('', '', '', broker_type=broker_type), None)

    msg: Message = MessageBuilder.build_message(message, params)

    assert msg.headers
    assert msg.data

    # Ensure that 'uuid', 'timestamp' and 'type' fields are present
    assert msg.headers.get('uuid')
    assert msg.headers.get('timestamp')
    assert msg.headers.get('type')

    assert msg.headers.get('type') == broker_type.name


@pytest.mark.parametrize("broker_type", [BrokerType.Private, BrokerType.Public])
def test_build_and_extract_message(broker_type):
    message: Dict = {'username': 'root', 'password': 'qwerty'}
    params = PubSubParams(Broker('', '', '', broker_type=broker_type), None)
    properties: BasicProperties = BasicProperties()
    properties.headers = {'type': broker_type.name}

    msg_orig: Message = MessageBuilder.build_message(message, params)
    msg_restored: Message = MessageBuilder.extract_message(properties, msg_orig.data)

    print(msg_orig.data)
    print(msg_restored.data)


