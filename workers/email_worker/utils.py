import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from config import AppConfig

# TODO: write logs to a custom file
logging.basicConfig(level=logging.INFO, format="{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M")
logger = logging.getLogger(__name__)


templates_path = os.path.join(AppConfig.STORAGE_PATH, "templates", "email")
template_env = Environment(loader=FileSystemLoader([templates_path]))

def generate_template(template_name: str, data: dict):
    template = template_env.get_template(name=f"{template_name}.html")
    return template.render(data)

def send_email(
    recipient: str,
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

            logger.info("Email delivered")

    except smtplib.SMTPAuthenticationError:
        logger.error(msg="Incorrect email or password", exc_info=True)
    except smtplib.SMTPConnectError:
        logger.error(
            msg="Failed to establish connection with smtp server",
            exc_info=True,
        )
    except smtplib.SMTPException:
        logger.error(msg="SMTP error", exc_info=True)
    except Exception as e:
        logger.error(msg=f"Failed to send email.\nError: {str(e)}")

def get_email_subject(event_type: str, email_data: dict):
    """Generate email subject using the email data as placeholders based on the type of event"""
    subjects = {
    "user_registered": f"Welcome to {AppConfig.APP_NAME}",
    "password_reset": f"Reset your {AppConfig.APP_NAME} Password",
    "welcome": f"Welcome to {AppConfig.APP_NAME}",
    "verification": f"Verify your email for {AppConfig.APP_NAME}"
    }

    # use custom subject if no subject has been configured and inject variables
    subject = subjects.get(event_type, f"New email from {AppConfig.APP_NAME}").format(*email_data)
    return subject


# use event type to fetch and route appropriate email
def dispatch_email(email_data: dict):
    """
    Send an email with the appropriate template using the event received
    """
    # compose email data
    email: str = email_data["email"]
    template_name: str = email_data["event_type"]
    template_data: dict[str, str] = email_data["data"]
    # compose email subject based on event type
    subject: str = get_email_subject(event_type=email_data["event_type"], email_data=template_data)

    # generate the template
    template: str | None = ""
    try:
        template = generate_template(template_name=template_name, data=template_data)
    except Exception as e:
        logger.error(f"Failed to generate template\nError: {str(e)}")

    # send the mail
    if template:
        send_email(recipient=email, subject=subject, template=template)
    else:
        logger.error(f"No template data found for event type: {template_name}")
    