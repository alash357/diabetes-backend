# app/utils/email_sender.py

import requests
from app.core.config import settings

def send_reset_email(email: str, reset_link: str):
    url = "https://api.sendgrid.com/v3/mail/send"

    payload = {
        "personalizations": [{"to": [{"email": email}]}],
        "from": {"email": settings.email_from},
        "subject": "🔐 Admin Password Reset",
        "content": [
            {
                "type": "text/html",
                "value": f"""
                <h2>Password Reset Request</h2>
                <p>Click the link below to reset your password. This link is valid for 1 hour.</p>
                <a href="{reset_link}" target="_blank">{reset_link}</a>
                <br /><br />
                <p>If you did not request this, you can ignore this email.</p>
                """
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {settings.sendgrid_api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 202:
        raise Exception(f"❌ Email sending failed: {response.status_code} - {response.text}")
