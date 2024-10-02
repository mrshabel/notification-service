import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr
from config import AppConfig
from schema import WelcomeEmailSchema, VerificationEmailSchema, NotificationEmailSchema, PasswordResetSchema, NotificationEventType

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

templates_path = os.path.join(AppConfig.STORAGE_PATH, "templates", "email")
env = Environment(loader=FileSystemLoader([templates_path]))

def generate_template(template_name: str, data: dict):
    template = env.get_template(name=f"{template_name}.html")
    return template.render(data)

def send_email(
    recipient: EmailStr,
    subject: str,
    template: str,
):
    message = MIMEMultipart()

    message["From"] = f"Shabel.io <{AppConfig.SMTP_USERNAME}>"
    message["To"] = recipient
    message["Subject"] = subject

    message.attach(MIMEText(template, "html"))

    try:
        with smtplib.SMTP(AppConfig.SMTP_SERVER, AppConfig.SMTP_PORT) as s:

            # send 'server hello' to initiate connection
            s.ehlo()

            # setup tls for encrypted security
            s.starttls()

            # login to mail account
            s.login(AppConfig.SMTP_USERNAME, AppConfig.SMTP_PASSWORD)

            s.sendmail(
                from_addr=AppConfig.SMTP_USERNAME,
                to_addrs=recipient,
                msg=message.as_string(),
            )

            logger.info("Message delivered")

    except smtplib.SMTPAuthenticationError:
        logger.error(msg="Incorrect email or password", exc_info=True)
        raise
    except smtplib.SMTPConnectError:
        logger.error(
            msg="Failed to establish connection with smtp server",
            exc_info=True,
        )
        raise
    except smtplib.SMTPException:
        logger.error(msg="SMTP error", exc_info=True)
        raise
    except Exception as e:
        logger.error(msg=f"An error occurred {str(e)}")
        raise

def send_verification_email(data: VerificationEmailSchema):
    template = generate_template("verify-email", data.model_dump())
    subject = "Verify your email address"
    
    # send the email
    send_email(recipient=data.email, subject=subject, template=template)

def send_welcome_email(data: WelcomeEmailSchema):
    template = generate_template("welcome", data.model_dump())
    subject = "Welcome"
    
    # send the email
    send_email(recipient=data.email, subject=subject, template=template)

def send_password_reset_email(data: PasswordResetSchema):
    template = generate_template("password-reset", data.model_dump())
    subject = "Password Reset Request"
    
    # send the email
    send_email(recipient=data.email, subject=subject, template=template)


def send_notification_email(data: NotificationEmailSchema):
    template = generate_template("notification", data.model_dump())
    subject = "Notification"
    
    # send the email
    send_email(recipient=data.email, subject=subject, template=template)


# use event type to fetch and route appropriate email
def dispatch_email(data: WelcomeEmailSchema | PasswordResetSchema | VerificationEmailSchema):
    """
    Send an email with the appropriate template using the event received
    """
    if data.type == NotificationEventType.WELCOME and isinstance(data, WelcomeEmailSchema):
        send_welcome_email(data)
    elif data.type == NotificationEventType.PASSWORD_RESET and isinstance(data, PasswordResetSchema):
        send_password_reset_email(data)
    elif data.type == NotificationEventType.VERIFICATION and isinstance(data, VerificationEmailSchema):
        send_verification_email(data)
    else:
        # TODO: send raw text as message
            logger.warning("Invalid event instance received")

    # match (data.type):
    #     case (NotificationEventType.WELCOME):
    #         send_welcome_email(data)
    #         pass
    #     case (NotificationEventType.PASSWORD_RESET):
    #         send_password_reset_email(data)
    #         pass
    #     case (NotificationEventType.VERIFICATION):
    #         send_verification_email(data)
    #         pass
    #     case (_):
    #         # TODO: send raw text as message
    #         logger.warning("Invalid event instance received")