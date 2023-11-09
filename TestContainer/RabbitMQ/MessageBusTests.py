import sys, os
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "..")
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../..")
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "../../..")

import time
from typing import List
from testcontainers.rabbitmq import RabbitMqContainer
from message_broker.Consumer_Thread_Queue import MessageBus
from message_broker.PubSubParams import Routing, Broker, PubSubParams


class TestsMessageBus:
    rabbitmq: RabbitMqContainer = None
    image_name: str = 'rabbitmq:latest'

    # Default RabbitMqContainer username/password pair:
    username: str = 'guest'
    password: str = 'guest'

    DEFAULT_RABBIT_AMQ_HOST: str = 'localhost'
    DEFAULT_RABBIT_AMQ_PORT: int = 5672
    DEFAULT_TOPIC_EXCHANGE: str = 'amq.topic'
    DEFAULT_VIRTUAL_HOST: str = '/'

    EVENTS_TOPIC: str = 'events'

    @classmethod
    def setup_class(cls):
        cls.rabbitmq = (RabbitMqContainer(image=cls.image_name)
                        .with_bind_ports(cls.DEFAULT_RABBIT_AMQ_PORT, cls.DEFAULT_RABBIT_AMQ_PORT).start())

        # credentials: PlainCredentials = PlainCredentials(cls.username, cls.password)
        # connection_params: ConnectionParameters = ConnectionParameters(
        #       host=cls.DEFAULT_RABBIT_AMQ_HOST, port=cls.DEFAULT_RABBIT_AMQ_PORT, virtual_host='/')

        cls.private_events: Routing = Routing(exchange=cls.DEFAULT_TOPIC_EXCHANGE, topic=cls.EVENTS_TOPIC,
                                              virtual_host=cls.DEFAULT_VIRTUAL_HOST)
        cls.broker_private: Broker = Broker(host=cls.DEFAULT_RABBIT_AMQ_HOST, port=cls.DEFAULT_RABBIT_AMQ_PORT,
                                            username=cls.username, password=cls.password)

    @classmethod
    def teardown_class(cls):
        cls.rabbitmq.stop()

    def test_publish_consume_one_message(self):
        params: PubSubParams = PubSubParams(self.broker_private, self.private_events)
        messages_to_send: List = [{'service': 'TestScheduler', 'user': 'root', 'password': '12345'}]
        messages_received: List = []

        def callback(msg) -> bool:
            messages_received.append(msg)
            return False

        def consume():
            consumer: MessageBus = MessageBus(callback=callback)
            consumer.add_consumers([params])
            consumer.start()

        def publish():
            time.sleep(0.25)
            for msg in messages_to_send:
                MessageBus.publish(msg, params)

        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(consume)
            executor.submit(publish)

        assert 1 == len(messages_received)

    def test_publish_consume_multiple_message(self):
        params: PubSubParams = PubSubParams(self.broker_private, self.private_events)

        msg_to_send: int = 10
        messages_to_send: List = [{'data': f'data_{i}'} for i in range(msg_to_send)]
        messages_received: List = []

        def callback(msg) -> bool:
            messages_received.append(msg)
            return msg_to_send > len(messages_received)

        def consume():
            consumer: MessageBus = MessageBus(callback=callback)
            consumer.add_consumers([params])
            consumer.start()

        def publish():
            time.sleep(0.25)
            for msg in messages_to_send:
                MessageBus.publish(msg, params)

        with ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(consume)
            executor.submit(publish)

        assert msg_to_send == len(messages_received)
        for msg in messages_to_send:
            # Ensure that we have received all messages which we have send
            assert any([str(msg) in str(m) for m in messages_received])
