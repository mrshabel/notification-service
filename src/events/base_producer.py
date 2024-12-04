from src.events import get_broker_channel
from src.config import settings


def publish_notification_to_worker(data: dict):
    """
    Route the notification to the appropriate worker based on the preferences
    """
    channel = get_broker_channel()
    channel.exchange_declare(
        settings.NOTIFICATION_EXCHANGE,
        exchange_type=settings.NOTIFICATION_EXCHANGE_TYPE,
    )
