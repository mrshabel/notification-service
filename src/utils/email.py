import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pydantic import EmailStr
from fastapi.logger import logger
from src.config import settings


def send_email(
    recipient: EmailStr,
    subject: str,
    template: str = "Welcome, this is a test email",
):
    message = MIMEMultipart()

    message["From"] = settings.SMTP_USERNAME
    message["To"] = recipient
    message["Subject"] = subject

    message.attach(MIMEText(template, "plain"))
    # message.attach(MIMEText(template, "html"))

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
