from . import BaseConsumer
from src.config import settings
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import logging
from threading import Thread, Event
from src.schemas.events import AuthEvents, Exchanges, Queues, ExchangeTypes
from src.events.handlers import AuthEventHandler
import time

# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pika")


class NotificationEventBus:
    def __init__(self, queue: str = Queues.NOTIFICATION.value):
        self.connection = None
        self.channel = None
        self.queue = queue
        self._running = False
        self._thread = None
        self._stop_event = Event()
        """ this event allows synchronization and communication among threads """

    def connect(self):
        """
        Establish a connection with the message broker
        """
        try:
            self.connection = BlockingConnection(
                ConnectionParameters(
                    host=settings.BROKER_HOST,
                    port=settings.BROKER_PORT,
                    heartbeat=0,
                )
            )
            # create channel
            self.channel = self.connection.channel()

            # declare queue and exchange bindings
            self._setup_bindings()
            logger.info("Connected to event bus successfully")
        except Exception as e:
            logger.error(f"Event bus connection error: {e}")
            raise e

    def _reconnect(self):
        """
        Initiate a reconnection to the event bus after 2 seconds on failure"""
        while not self._stop_event.is_set():
            try:
                # disconnect and reconnect
                self.disconnect()
                self.connect()
            except BaseException:
                logger.warning("Reconnection to event bus failed. Retrying...")
                time.sleep(2)

    def disconnect(self):
        try:
            if self.channel and self.channel.is_open:
                self.channel.close()
                self.channel = None

            if self.connection and self.connection.is_open:
                self.connection.close()
                self.connection = None

            logger.info("Disconnected from event bus")
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")

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
            durable=True,
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
                data = AuthEventHandler.process_event(body=body)
                print(data, flush=True)
                logger.info("Sent to auth handler")

            else:
                logger.warning(
                    f"No handler implemented for event with routing key: {method.routing_key}"
                )

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
        # check if thread has not started
        while not self._stop_event.is_set():
            try:
                self.connect()
                self._consume()
            except BaseException:
                logger.warning(
                    "Connection to broker lost. Attempting to reconnect..."
                )
                self._reconnect()

    def start(self):
        """
        Start event bus on new thread
        """
        # check if process is already running in thread
        if self._running:
            logger.warning("Event bus is already running")
            return

        # block all waiting threads
        self._stop_event.clear()

        # run thread as daemon: shutdown thread when main thread stops
        self._thread = Thread(target=self._start_consuming, daemon=True)
        self._thread.start()

        self._running = True
        logger.info("Event bus started successfully")

    def stop(self, timeout=2):
        if not self._running:
            logger.warning("Event bus is not running")
            return

        logger.info("Stopping event bus...")
        self._stop_event.set()

        try:
            if self._thread:
                self._thread.join(timeout)
        except Exception as e:
            logger.error(f"Error stopping event bus thread: {e}")
