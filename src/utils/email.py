import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pydantic import EmailStr
from fastapi.logger import logger
from src.config import settings
from src.utils import template


def send_email(
    recipient: EmailStr,
    subject: str,
    template: str = "Welcome, this is a test email",
):
    message = MIMEMultipart()

    message["From"] = settings.SMTP_USERNAME
    message["To"] = recipient
    message["Subject"] = subject

    message.attach(MIMEText(template, "html"))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as s:

            # send 'server hello' to initiate connection
            s.ehlo()

            # setup tls for encrypted security
            s.starttls()

            # login to mail account
            s.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)

            s.sendmail(
                from_addr=settings.SMTP_USERNAME,
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


def send_welcome_email(recipient: EmailStr):
    subject: str = "Welcome to Shabel's World"
    data = {}

    # generate html template
    html_template = template.generate_template("welcome.html", data=data)

    # send email
    send_email(recipient=recipient, subject=subject, template=html_template)


def send_verify_email(recipient: EmailStr, name: str):
    subject: str = "Verify your account"
    data = {"name": name}

    # generate html template
    html_template = template.generate_template("verify-email.html", data=data)

    # send email
    send_email(recipient=recipient, subject=subject, template=html_template)
