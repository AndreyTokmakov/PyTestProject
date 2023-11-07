import sys
import pika

from collections.abc import Callable
from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic
from queue import Empty, Queue
from threading import Thread, Event
from typing import Any, List, Dict
from message_broker.PubSubParams import PubSubParams, Broker, Routing
from message_broker.Message import MessageBuilder, Message


class MessageBus(object):

    def __init__(self, callback) -> None:
        self.message_queue: Queue = Queue()
        self.consumers: List[Thread] = []
        self.callback: Callable[Any, None] = callback
        self.event: Event = Event()

    def add_consumers(self, pub_sub_params: List[PubSubParams]) -> None:
        for param in pub_sub_params:
            self.consumers.append(Thread(target=self.consume_from_topic, args=(param,)))

    def message_received(self,
                         channel: BlockingChannel,
                         method: Basic.Deliver,
                         properties: BasicProperties,
                         body: bytes) -> None:

        msg: Message = MessageBuilder.extract_message(properties, body)
        self.message_queue.put([msg.data, msg.headers, [method.exchange, method.routing_key]])

    def process_queue(self) -> None:
        while not self.event.is_set():
            try:
                item: Any = self.message_queue.get(timeout=0.5)
                self.callback(item)
            except Empty:
                continue

    def consume_from_topic(self,
                           params: PubSubParams):
        broker: Broker = params.broker
        routing: Routing = params.routing
        with pika.BlockingConnection(pika.ConnectionParameters(host=broker.host,
                                                               port=broker.port,
                                                               virtual_host=routing.virtual_host,
                                                               ssl_options=broker.ssl_options,
                                                               credentials=broker.credentials)) as connection:
            channel: BlockingChannel = connection.channel()
            channel.exchange_declare(exchange=routing.exchange,
                                     durable=routing.durable,
                                     exchange_type=routing.exchange_type.value)

            result = channel.queue_declare(queue=routing.topic, exclusive=False)
            channel.queue_bind(exchange=routing.exchange, queue=routing.topic)
            channel.basic_consume(queue=routing.topic,
                                  on_message_callback=self.message_received,
                                  auto_ack=True)

            channel.start_consuming()

    def start(self):
        for thread in self.consumers:
            thread.start()
        try:
            self.process_queue()
        except KeyboardInterrupt:
            # TODO: Save data in the message_queue to some file maybe.... someday
            sys.exit(0)

    @staticmethod
    def publish(message: Dict,
                params: PubSubParams):
        broker: Broker = params.broker
        routing: Routing = params.routing
        with pika.BlockingConnection(pika.ConnectionParameters(host=broker.host,
                                                               port=broker.port,
                                                               virtual_host=routing.virtual_host,
                                                               credentials=broker.credentials)) as connection:
            channel: BlockingChannel = connection.channel()
            msg: Message = MessageBuilder.build_message(message, params)

            channel.basic_publish(exchange=routing.exchange,
                                  routing_key=routing.topic,
                                  properties=pika.BasicProperties(headers=msg.headers),
                                  body=msg.data)


