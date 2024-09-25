import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, PackageLoader, FileSystemLoader
from pydantic import EmailStr
from config import AppConfig
from schema import WelcomeEmailSchema, VerificationEmailSchema, NotificationEmailSchema, PasswordResetSchema

templates_path = os.path.join(AppConfig.STORAGE_PATH.value, "templates", "email")
env = Environment(loader=FileSystemLoader([templates_path]))

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def generate_template(template_name: str, data: dict):
    template = env.get_template(name=f"{template_name}.html")
    return template.render(data)

def send_email(
    recipient: EmailStr,
    subject: str,
    template: str,
):
    message = MIMEMultipart()

    message["From"] = f"Shabel.io <{AppConfig.SMTP_USERNAME.value}>"
    message["To"] = recipient
    message["Subject"] = subject

    message.attach(MIMEText(template, "html"))

    try:
        with smtplib.SMTP(AppConfig.SMTP_SERVER.value, AppConfig.SMTP_PORT.value) as s:

            # send 'server hello' to initiate connection
            s.ehlo()

            # setup tls for encrypted security
            s.starttls()

            # login to mail account
            s.login(AppConfig.SMTP_USERNAME.value, AppConfig.SMTP_PASSWORD.value)

            s.sendmail(
                from_addr=AppConfig.SMTP_USERNAME.value,
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
    template = generate_template("verify-email", data)
    subject = "Verify your email address"
    
    # send the email
    send_email(recipient=data.email, subject=subject, template=template)

def send_welcome_email(data: WelcomeEmailSchema):
    template = generate_template("welcome", data)
    subject = "Welcome"
    
    # send the email
    send_email(recipient=data.email, subject=subject, template=template)

def send_password_reset_email(data: WelcomeEmailSchema):
    template = generate_template("password-reset", data)
    subject = "Password Reset Request"
    
    # send the email
    send_email(recipient=data.email, subject=subject, template=template)


def send_notification_email(data: NotificationEmailSchema):
    template = generate_template("notification", data)
    subject = "Notification"
    
    # send the email
    send_email(recipient=data.email, subject=subject, template=template)
