import datetime
import time
from threading import Thread
from typing import Dict, List

import pika
from pika.exchange_type import ExchangeType
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic
from pika import BasicProperties
from testcontainers.rabbitmq import RabbitMqContainer

from TestContainer.RabbitMQ.message_broker.Consumer_Thread_Queue import MessageBus
from TestContainer.RabbitMQ.message_broker.PubSubParams import Routing, Broker, PubSubParams


def process_message(msg) -> bool:
    print("--" * 100)
    print(msg)
    return True


def message_received(channel: BlockingChannel,
                     method: Basic.Deliver,
                     properties: BasicProperties,
                     body: bytes):
    process_message(body.decode(encoding='utf-8'))
    # channel.stop_consuming()


def check_params():
    with RabbitMqContainer(image="rabbitmq:latest") as rabbitmq:
        params: pika.ConnectionParameters = rabbitmq.get_connection_params()
        with pika.BlockingConnection(params) as connection:
            channel = connection.channel()
            credentials: pika.credentials.PlainCredentials = params.credentials
            print(f'host: {params.host}, port: {params.port}, '
                  f'virtual_host: {params.virtual_host}, username: {credentials.username}, password: {credentials.password}')


def try_publish_simple():
    with RabbitMqContainer(image="rabbitmq:latest") as rabbitmq:
        params: pika.ConnectionParameters = rabbitmq.get_connection_params()
        with pika.BlockingConnection(params) as connection:
            channel = connection.channel()
            channel.queue_declare(queue='hello')
            channel.basic_publish(exchange='', routing_key='hello', body=b'Hello W0rld!')


def try_consume_simple():
    exchange_name: str = 'amq.topic'
    topic: str = 'events'
    with RabbitMqContainer(image="rabbitmq:latest") as rabbitmq:
        connection_params: pika.ConnectionParameters = rabbitmq.get_connection_params()
        credentials: pika.credentials.PlainCredentials = connection_params.credentials

        print(f'host: {connection_params.host}, port: {connection_params.port}, virtual_host: {connection_params.virtual_host}, '
              f'username: {credentials.username}, password: {credentials.password}')

        with pika.BlockingConnection(connection_params) as connection:
            channel: BlockingChannel = connection.channel()
            channel.exchange_declare(exchange=exchange_name,
                                     durable=True,
                                     exchange_type=ExchangeType.topic)
            result = channel.queue_declare(queue=topic, exclusive=False)
            print(result)
            channel.queue_bind(exchange=exchange_name, queue=topic)
            channel.basic_consume(queue=topic,
                                  on_message_callback=message_received,
                                  auto_ack=True)

            channel.start_consuming()


def publish_consume():
    with RabbitMqContainer(image="rabbitmq:latest") as rabbitmq:
        connection_params: pika.ConnectionParameters = rabbitmq.get_connection_params()
        credentials: pika.credentials.PlainCredentials = connection_params.credentials

        private_events = Routing(exchange='amq.topic', topic='events', virtual_host=connection_params.virtual_host)
        broker_private: Broker = Broker(host=connection_params.host, port=connection_params.port,
                                        username=credentials.username, password=credentials.password)
        params: PubSubParams = PubSubParams(broker_private, private_events)

        def consume_thread():
            with pika.BlockingConnection(connection_params) as connection:
                routing: Routing = params.routing
                channel: BlockingChannel = connection.channel()
                channel.exchange_declare(exchange=routing.exchange, durable=routing.durable, exchange_type=ExchangeType.topic)
                result = channel.queue_declare(queue=routing.topic, exclusive=False)
                channel.queue_bind(exchange=routing.exchange, queue=routing.topic)
                channel.basic_consume(queue=routing.topic, on_message_callback=message_received, auto_ack=True)
                channel.start_consuming()

        def publish_thread():
            time.sleep(0.1)
            with pika.BlockingConnection(connection_params) as connection:
                routing: Routing = params.routing
                channel: BlockingChannel = connection.channel()
                msg = f'Hello from {datetime.datetime.utcnow()}'
                channel.basic_publish(exchange=routing.exchange,
                                      routing_key=routing.topic,  # Send to queue's of 'test_exchange1' channel
                                      body=bytes(msg, encoding='utf8'))

        t1: Thread = Thread(target=consume_thread)
        t2: Thread = Thread(target=publish_thread)
        t1.start()
        t2.start()

        t1.join()


def publish_consume_lib():
    with RabbitMqContainer(image="rabbitmq:latest") as rabbitmq:
        connection_params: pika.ConnectionParameters = rabbitmq.get_connection_params()
        credentials: pika.credentials.PlainCredentials = connection_params.credentials

        private_events = Routing(exchange='amq.topic', topic='events', virtual_host=connection_params.virtual_host)
        broker_private: Broker = Broker(host=connection_params.host, port=connection_params.port,
                                        username=credentials.username, password=credentials.password)
        params: PubSubParams = PubSubParams(broker_private, private_events)
        messages: List = []

        counter: int = 0

        def callback(msg) -> bool:
            messages.append(msg)
            nonlocal counter
            counter += 1

            return 2 > counter

        def consume_thread():
            consumer: MessageBus = MessageBus(callback=callback)
            consumer.add_consumers([params])
            consumer.start()

        def publish_thread():
            time.sleep(0.1)
            msg: Dict = {'service': 'TestScheduler', 'user': 'root', 'password': '12345'}
            MessageBus.publish(msg, params)
            MessageBus.publish(msg, params)

        t1: Thread = Thread(target=consume_thread)
        t2: Thread = Thread(target=publish_thread)
        t1.start()
        t2.start()
        t1.join()

        print(messages)


if __name__ == '__main__':
    # check_params()
    # try_publish_simple()
    # try_consume_simple()

    # publish_consume()

    publish_consume_lib()
