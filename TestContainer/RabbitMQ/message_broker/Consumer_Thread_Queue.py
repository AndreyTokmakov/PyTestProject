import pika

from pika.exceptions import AMQPError
from pika import BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic
from queue import Empty, Queue
from threading import Thread, Event
from typing import Any, List, Dict, Tuple, Callable
from message_broker.PubSubParams import PubSubParams, Broker, Routing
from message_broker.Message import MessageBuilder, Message


class MessageBus(object):
    QUEUE_POLL_TIMEOUT: float = 0.5

    def __init__(self, callback: Callable[[Any], bool]) -> None:
        self.message_queue: Queue[Tuple[Any, BlockingChannel]] = Queue()
        self.consumers: List[Thread] = []
        self.callback: Callable[[Any], bool] = callback

    def add_consumers(self, pub_sub_params: List[PubSubParams]) -> None:
        for param in pub_sub_params:
            self.consumers.append(Thread(target=self.consume_from_topic, args=(param,)))

    def message_received(self,
                         channel: BlockingChannel,
                         method: Basic.Deliver,
                         properties: BasicProperties,
                         body: bytes) -> None:

        msg: Message = MessageBuilder.extract_message(properties, body)
        self.message_queue.put(([msg.data, msg.headers, [method.exchange, method.routing_key]], channel))

    def process_queue(self) -> None:
        while True:
            try:
                payload, channel = self.message_queue.get(timeout=MessageBus.QUEUE_POLL_TIMEOUT)
                if not self.callback(payload):
                    try:
                        channel.stop_consuming()
                    except AMQPError as _:
                        pass
                    break
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

            result = channel.queue_declare(queue=routing.topic, exclusive=False, durable=routing.durable)
            channel.queue_bind(exchange=routing.exchange, queue=routing.topic)
            channel.basic_consume(queue=routing.topic,
                                  on_message_callback=self.message_received,
                                  auto_ack=True)
            try:
                channel.start_consuming()
            except AMQPError as _:
                pass

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
