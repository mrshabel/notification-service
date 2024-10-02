from . import BaseConsumer
from src.config import settings
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import logging
from threading import Thread
from src.schemas.events import AuthEvents, Exchanges, Queues, ExchangeTypes
from src.events.handlers import AuthEventHandler

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("pika")


class NotificationEventBus:
    def __init__(self, queue: str = Queues.NOTIFICATION.value):
        self.connection = None
        self.channel = None
        self.queue = queue

    def connect(self):
        """
        Establish a connection with the message broker
        """
        try:
            self.connection = BlockingConnection(
                ConnectionParameters(
                    host=settings.BROKER_HOST, port=settings.BROKER_PORT
                )
            )
            # create channel
            self.channel = self.connection.channel()

            # declare queue and exchange bindings
            self._setup_bindings()
            logger.info("Connected to broker successfully")
        except Exception as e:
            logger.error(f"Broker connection error: {e}")
            raise e

    def disconnect(self):
        """
        Close connection and channel
        """
        try:
            if self.channel and self.channel.is_open:
                self.channel.close()
                logger.info("Channel closed successfully")

            if self.connection and self.connection.is_open:
                self.connection.close()
                logger.info("Connection closed successfully")
        except Exception as e:
            logger.error(f"Error closing broker connection")
            raise e

    def _setup_bindings(self):
        """
        Declare primary notification queue and bind the exchanges from other services to the queue
        """
        AUTH_ROUTING_KEYS = [routing_key.value for routing_key in AuthEvents]

        self.channel.queue_declare(self.queue, durable=True)

        # bind queue to exchange with provided routing keys
        self.channel.exchange_declare(
            exchange=Exchanges.AUTH.value,
            exchange_type=ExchangeTypes.AUTH.value,
        )

        # auth bindings
        for routing_key in AUTH_ROUTING_KEYS:
            self.channel.queue_bind(
                queue=self.queue,
                exchange=Exchanges.AUTH.value,
                routing_key=routing_key,
            )

    def _consumer_callback(
        self,
        ch: BlockingChannel,
        method: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ):
        """
        Consume messages and send event to appropriate handlers
        """
        try:
            logger.info("processing....")

            # handle auth events
            if method.routing_key.startswith("auth"):
                AuthEventHandler.process_event(body=body)
                logger.info("Sent to auth handler")
            
            else:
                logger.warning(f"No handler implemented for event with routing key: {method.routing_key}")

            # send acknowledgement that message is done processing
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info("processing finished")
        except Exception as e:
            logger.error(f"Failed to process event: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            # raise e

    def _consume(self):
        """
        Start consuming messages from the queue
        """
        # process only 1 message at a time
        # self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self._consumer_callback
        )
        self.channel.start_consuming()
        logger.info(f"Consuming messages from: {self.queue}")

    def _start_consuming(self):
        self.connect()
        self._consume()

    def start(self):
        """
        Start event bus on new thread
        """
        task = Thread(target=self._start_consuming, daemon=True)
        task.start()
