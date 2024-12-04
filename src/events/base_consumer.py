from src.config import settings
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import logging
from threading import Thread

# from concurrent.futures import ThreadPoolExecutor
# from multiprocessing import cpu_count
# from . import main as main_consumer
# from threading import Lock

# lock = Lock()


# def start_consumers():
#     """
#     Spin up a threadpool to execute all consumers in the application
#     """
#     # max_workers = cpu_count() if cpu_count else 2
#     with ThreadPoolExecutor(max_workers=2) as executor:
#         with lock:
#             # protect shared resources
#             # submit consumers
#             executor.submit(main_consumer.consume_main_queue).result()

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("pika")


class BaseConsumer:
    def __init__(
        self,
        queue: str,
        exchange: str,
        exchange_type: str,
        routing_keys: list[str],
    ):
        self.connection = None
        self.channel = None
        self.queue = queue
        self.exchange = exchange
        self.routing_keys = routing_keys

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
            self._setup_queue_bindings()
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

    def _setup_queue_bindings(self):
        """
        Declare queue and bind to exchange with routing keys if provided
        """
        self.channel.queue_declare(self.queue, durable=True)

        # bind queue to exchange with provided routing keys
        for routing_key in self.routing_keys:
            self.channel.queue_bind(
                queue=self.queue,
                exchange=self.exchange,
                routing_key=routing_key,
            )

    def consume(self, callback):
        """
        Start consuming messages from the queue
        """
        # process only 1 message at a time
        # self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=callback
        )
        self.channel.start_consuming()
        logger.info(f"Consuming messages from: {self.queue}")

    def start(self):
        """
        Start consumer in new thread
        """
        task = Thread(target=self.consume, daemon=True)
        task.start()
