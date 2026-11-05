"""HealthSecure Email Dispatch Service.

Handles secure SMTP dispatch of PDF prediction reports with MIME attachments,
environment-based configuration, input validation, and safe error handling.
"""

from __future__ import annotations

import io
import logging
import os
import re
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Tuple, Union

logger = logging.getLogger("healthsecure.email")

EMAIL_REGEX = re.compile(r"^[\w\.\+-]+@([\w-]+\.)+[\w-]{2,10}$")


def is_valid_email(email: str) -> bool:
    """Validate email address format."""
    if not email or len(email) > 254:
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def is_smtp_configured() -> bool:
    """Check whether SMTP environment variables are properly configured."""
    server = os.environ.get("MAIL_SERVER", "").strip()
    username = os.environ.get("MAIL_USERNAME", "").strip()
    password = os.environ.get("MAIL_PASSWORD", "").strip()
    return bool(server and (password or username))


def send_prediction_report_email(
    recipient_email: str,
    recipient_name: str,
    pdf_buffer: Union[io.BytesIO, bytes, None] = None,
    prediction_id: int = 1,
    estimated_premium: float | None = None,
    pdf_bytes: bytes | None = None,
    filename: str | None = None,
) -> Tuple[bool, str]:
    """Send generated PDF prediction report to user's email via SMTP.

    Returns:
        (success: bool, message: str)
    """
    if not recipient_email or not is_valid_email(recipient_email):
        return False, "Invalid recipient email address format."

    # Normalize buffer from either pdf_buffer or pdf_bytes
    if pdf_buffer is None and pdf_bytes is not None:
        buf = io.BytesIO(pdf_bytes)
    elif isinstance(pdf_buffer, bytes):
        buf = io.BytesIO(pdf_buffer)
    elif isinstance(pdf_buffer, io.BytesIO):
        buf = pdf_buffer
    else:
        buf = io.BytesIO(b"%PDF-1.4 mock prediction report")

    mail_server = os.environ.get("MAIL_SERVER", "").strip()
    mail_port = int(os.environ.get("MAIL_PORT", "587"))
    mail_use_tls = os.environ.get("MAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
    mail_use_ssl = os.environ.get("MAIL_USE_SSL", "False").lower() in ("true", "1", "yes") or mail_port == 465
    mail_username = os.environ.get("MAIL_USERNAME", "").strip()
    mail_password = os.environ.get("MAIL_PASSWORD", "").strip()
    default_sender = os.environ.get(
        "MAIL_DEFAULT_SENDER",
        f"HealthSecure AI <{mail_username or 'noreply@healthsecure.com'}>"
    )

    clean_name = (recipient_name or "Valued Member").strip()

    # Academic Project Disclaimer
    disclaimer = (
        "\n\n------------------------------------------------------------\n"
        "Academic Project Disclaimer:\n"
        "HealthSecure is an educational research project applying machine learning "
        "to estimate simulated medical costs. This report does not represent an official "
        "insurance quotation or binding insurance policy."
    )

    body_text = (
        f"Hello {clean_name},\n\n"
        "Your HealthSecure premium prediction report is attached to this email.\n\n"
        "You can review your estimated premium and the sample insurance plans "
        "suggested by the application."
    )
    if estimated_premium:
        body_text += f"\n\nEstimated Annual Premium: INR {estimated_premium:,.2f}"

    body_text += (
        "\n\nRegards,\n"
        "HealthSecure Team\n"
        "Smart Insurance Prediction Powered by Machine Learning"
        f"{disclaimer}"
    )

    # If SMTP is not yet configured in .env, simulate gracefully for demonstration
    # Check for placeholder / demo domains or testing environment
    # to avoid SMTP delivery failures, bounce timeouts, and sender reputation degradation.
    demo_domains = {"healthsecure.com", "example.com", "test.com", "healthsecure.local", "demo.local"}
    email_domain = recipient_email.strip().lower().split("@")[-1]
    is_testing = os.environ.get("FLASK_ENV") == "testing" or os.environ.get("TESTING") == "True"

    if email_domain in demo_domains or is_testing:
        logger.info(
            f"[SMTP Simulated Mode] Report #{prediction_id} simulated for demo/test recipient {recipient_email}."
        )
        return True, (
            f"Email simulated: PDF Report #{prediction_id} generated for demo account ({recipient_email}). "
            "To receive a live email, enter an active personal email address (e.g., your Gmail)."
        )

    if not is_smtp_configured():
        logger.info(
            f"[SMTP Simulated Mode] Report #{prediction_id} prepared for {recipient_email}. "
            "SMTP server/credentials not configured in .env."
        )
        return True, (
            f"Email simulated: PDF Report #{prediction_id} generated for {recipient_email}. "
            "Configure MAIL_SERVER and MAIL_PASSWORD in .env to dispatch live emails."
        )

    # Compose MIME message
    try:
        msg = MIMEMultipart()
        msg["From"] = default_sender
        msg["To"] = recipient_email
        msg["Subject"] = "Your HealthSecure Premium Prediction Report"

        msg.attach(MIMEText(body_text, "plain", "utf-8"))

        # Attach PDF
        buf.seek(0)
        attachment = MIMEApplication(buf.read(), _subtype="pdf")
        attach_fname = filename or f"healthsecure-report-{prediction_id}.pdf"
        attachment.add_header("Content-Disposition", "attachment", filename=attach_fname)
        msg.attach(attachment)

        # Connect and send
        if mail_use_ssl:
            with smtplib.SMTP_SSL(mail_server, mail_port, timeout=15) as server:
                if mail_username and mail_password:
                    server.login(mail_username, mail_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(mail_server, mail_port, timeout=15) as server:
                server.ehlo()
                if mail_use_tls:
                    server.starttls()
                    server.ehlo()
                if mail_username and mail_password:
                    server.login(mail_username, mail_password)
                server.send_message(msg)

        logger.info(f"Successfully emailed report #{prediction_id} to {recipient_email}")
        return True, f"Prediction report #{prediction_id} has been dispatched to {recipient_email}."

    except smtplib.SMTPAuthenticationError as auth_err:
        logger.error(f"SMTP Authentication Error for {recipient_email}: {auth_err}")
        return False, "SMTP authentication failed. Please verify MAIL_USERNAME and MAIL_PASSWORD in .env."
    except (smtplib.SMTPException, OSError) as smtp_err:
        logger.error(f"SMTP dispatch failed for {recipient_email}: {smtp_err}")
        return False, f"Email delivery failed: {smtp_err}"
    except Exception as exc:
        logger.error(f"Unexpected error sending prediction email: {exc}")
        return False, f"Unexpected error dispatching report: {exc}"
