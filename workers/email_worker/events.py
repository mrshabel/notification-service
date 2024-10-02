import pika
import json
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from config import AppConfig
from utils import logger, dispatch_email
from schema import BaseEmailSchema, NotificationEventType, WelcomeEmailSchema, PasswordResetSchema, VerificationEmailSchema

def start_email_consumer():
    """
    Start the email consumer on the main thread for message listening
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=AppConfig.BROKER_HOST, port=AppConfig.BROKER_PORT))
    channel = connection.channel()

    channel.exchange_declare(exchange=AppConfig.NOTIFICATION_EXCHANGE, exchange_type="direct")

    channel.queue_declare(queue=AppConfig.EMAIL_QUEUE)

    # bind to the notification exchange. this will allow delivery of only interested events
    channel.queue_bind(exchange=AppConfig.NOTIFICATION_EXCHANGE, queue=AppConfig.EMAIL_QUEUE, routing_key=AppConfig.EMAIL_ROUTING_KEY)

    # start consuming
    logger.info("[*] Waiting for email events to process")

    channel.basic_consume(queue=AppConfig.EMAIL_QUEUE, on_message_callback=callback)
    channel.start_consuming()

def callback(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    logger.info("[*] Message received. waiting to process")
    data = json.loads(body)

    # dispatch email
    match (data["type"]):
        case (NotificationEventType.WELCOME):
            email_data = WelcomeEmailSchema(**vars(data))
        case (NotificationEventType.PASSWORD_RESET):
            email_data = PasswordResetSchema(**vars(data))
        case (NotificationEventType.VERIFICATION):
            email_data = VerificationEmailSchema(**vars(data))
        case (_):
            logger.warning("Invalid event type received")
            return
    
    try:
        # process the email
        dispatch_email(data=email_data)

        # acknowledge on success
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info(f"Email sent successfully")
    except Exception as e:
        # raise exception
        logger.error(str(e))
        ch.basic_nack(delivery_tag=method.delivery_tag)
        raise e
