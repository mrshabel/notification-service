from utils import send_welcome_email
from schema import WelcomeEmailSchema
from events import start_email_consumer
from time import sleep

def main():
    # a test mail to the recipient address
    # send_welcome_email(WelcomeEmailSchema(email="bawesad120@sgatra.com"))
    while True:
        start_email_consumer()
        # restart worker after 500ms
        sleep(0.5)


if __name__ == "__main__":
    main()