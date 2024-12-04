import pika
import json
from time import sleep
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from config import AppConfig
from utils import logger, dispatch_email

# start the consumer
def start_email_consumer():
    """
    Start the email consumer on the main thread for message listening
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=AppConfig.BROKER_HOST, port=AppConfig.BROKER_PORT))
    channel = connection.channel()

    # REFACTOR: move declarations into definitions.json to declare the configuration on application startup rather than allowing individual clients to do so
    channel.exchange_declare(exchange=AppConfig.NOTIFICATION_EXCHANGE, exchange_type="topic")

    channel.queue_declare(queue=AppConfig.EMAIL_QUEUE)

    # bind to the notification exchange. this will allow delivery of only interested events
    channel.queue_bind(exchange=AppConfig.NOTIFICATION_EXCHANGE, queue=AppConfig.EMAIL_QUEUE, routing_key=AppConfig.EMAIL_ROUTING_KEY)

    # start consuming
    logger.info("[*] Waiting for email events to process")

    channel.basic_consume(queue=AppConfig.EMAIL_QUEUE, on_message_callback=process_email)
    channel.start_consuming()

# 
def process_email(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    logger.info("[*] Message received. waiting to process")

    # sample data (email, event_type, data)
    data = json.loads(body)
    
    # dispatch email
    try:
        # process the email
        dispatch_email(email_data=data)

        # acknowledge on success
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"Event processed")

    except Exception as e:
        logger.error(f"Failed to process event. {str(e)}")

        # raise exception and send no acknowledgement
        ch.basic_nack(delivery_tag=method.delivery_tag)
        raise e
     


if __name__ == "__main__":
    # a test mail to the recipient address
    while True:
        try:
            start_email_consumer()
        # restart worker after 500ms
        except BaseException as e:
            sleep(0.5)