from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from src.schemas.events import BrokerQueues
from src.config import settings
from threading import Thread
import logging

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger("pika")

def consume_main_queue():
    # create a new channel to run consumer on
    try:
        connection = BlockingConnection(
            ConnectionParameters(host=settings.BROKER_HOST, port=settings.BROKER_PORT)
        )
        channel = connection.channel()
        # ensure queue exists
        channel.queue_declare(queue=BrokerQueues.MAIN.value, durable=True)
        logger.info("Waiting for messages")
    except Exception as e:
        logger.error(
            f"Failed to establish connection with with message broker: {str(e)}"
        )
        raise e

    # process only 1 item in consumer at a time to avoid message overload on 1 consumer (Fair Load Distribution)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=BrokerQueues.MAIN.value, on_message_callback=callback
    )
    channel.start_consuming()


def callback(
    ch: BlockingChannel,
    method: Basic.Deliver,
    properties: BasicProperties,
    body: bytes,
):
    logger.info(f" [x] Received {body.decode()}")
    try:
        logger.info("processing....")
        # send acknowledgement that message is done processing
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("processing finished")
    except Exception as e:
        logger.error(f"Failed to process event: {str(e)}")
        ch.basic_nack(delivery_tag=method.delivery_tag)
        raise e

def start_main_consumer():
    """
    Spin a new thread to run the main consumer on application startup
    """
    task = Thread(target=consume_main_queue, daemon=True)
    task.start()