from pika import BlockingConnection, ConnectionParameters
from src.config import settings
from fastapi.logger import logger

connection: BlockingConnection


def start_broker_connection():
    global connection
    connection = BlockingConnection(
        ConnectionParameters(
            host=settings.BROKER_HOST, port=settings.BROKER_PORT
        )
    )
    logger.info("Message broker successfully connected")


def get_broker_channel():
    """
    Retrieve the current communication channel to process all requests
    """
    global connection
    if connection and connection.is_open:
        return connection.channel()


def close_broker_connection():
    global connection
    if connection and connection.is_open:
        connection.close()
        logger.info("Message broker connection closed")
