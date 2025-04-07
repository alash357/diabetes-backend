# app/core/email_service.py

from fastapi import BackgroundTasks
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.core.config import settings
import os

# Setup Jinja2 environment
templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
jinja_env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(['html', 'xml'])
)

def send_reset_email_background(
    background_tasks: BackgroundTasks, 
    to_email: str, 
    reset_token: str
):
    background_tasks.add_task(send_reset_email, to_email, reset_token)

def send_reset_email(to_email: str, reset_token: str):
    template = jinja_env.get_template("reset_password.html")
    html_content = template.render(token=reset_token)

    message = Mail(
        from_email=settings.smtp_sender_email,
        to_emails=to_email,
        subject="Reset your password",
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(settings.sendgrid_api_key)
        sg.send(message)
    except Exception as e:
        print(f"Failed to send email: {e}")
