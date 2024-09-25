from utils import send_welcome_email
from schema import WelcomeEmailSchema

def main():
    # a test mail to the recipient address
    send_welcome_email(WelcomeEmailSchema(email="bawesad120@sgatra.com"))


if __name__ == "__main__":
    main()