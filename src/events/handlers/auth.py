import json


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
        return data
