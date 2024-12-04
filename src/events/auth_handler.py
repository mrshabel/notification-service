import json
from src.events import get_broker_channel
from src.config import settings
from fastapi.logger import logger

class AuthEventHandler:
    """
    Helper method class to process all auth events
    """

    @staticmethod
    def process_event(body: bytes):
        """
        Process events received from the authentication service
        """
        data = json.loads(body)
        # process data

        # get user channels
        user_channels = ["email", "inapp"]

        # broadcast data to channels
        for channel in user_channels:
            AuthEventHandler.publish_to_channel(channel, data)


    @staticmethod
    def publish_to_channel(channel: str, data: dict):
        """Send auth notification event to the user's subscribed channels"""
        try:
            channel = get_broker_channel()

            # compose routing key in format "notification.auth.<channel>"
            routing_key = f"notification.auth.{channel}"

            # publish data to channel
            channel.basic_publish(exchange=settings.NOTIFICATION_EXCHANGE, routing_key=routing_key, body=data)
        except BaseException as e:
            logger.error(f"Fatal error: Failed to publish event to channel", exc_info=True)