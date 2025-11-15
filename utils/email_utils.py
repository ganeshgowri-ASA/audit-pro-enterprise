"""
Email utility functions for sending notifications
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import config

def send_email(to_email, subject, body, html_body=None):
    """
    Send email notification

    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Plain text body
        html_body: HTML body (optional)

    Returns:
        bool: True if successful, False otherwise
    """
    if not config.SMTP_USER or not config.SMTP_PASSWORD:
        print("Email configuration not set. Skipping email notification.")
        return False

    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = config.EMAIL_FROM
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add plain text and HTML parts
        msg.attach(MIMEText(body, 'plain'))
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))

        # Connect to SMTP server and send
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.send_message(msg)

        print(f"Email sent successfully to {to_email}")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_nc_ofi_assignment_email(nc_ofi, assignee):
    """
    Send email notification when NC/OFI is assigned

    Args:
        nc_ofi: NCOFI model instance
        assignee: User model instance
    """
    subject = f"[Audit Pro] New {nc_ofi.type} Assigned: {nc_ofi.severity} - {nc_ofi.clause_no}"

    body = f"""
Hello {assignee.full_name},

You have been assigned a new {nc_ofi.type} finding:

Finding ID: {nc_ofi.id}
Type: {nc_ofi.type}
Severity: {nc_ofi.severity}
Clause: {nc_ofi.clause_no}
Description: {nc_ofi.description}
Due Date: {nc_ofi.due_date.strftime('%Y-%m-%d') if nc_ofi.due_date else 'Not set'}
Status: {nc_ofi.status}

Please review and take necessary action.

---
Audit Pro Enterprise
"""

    html_body = f"""
<html>
<body>
    <p>Hello {assignee.full_name},</p>

    <p>You have been assigned a new <strong>{nc_ofi.type}</strong> finding:</p>

    <table style="border-collapse: collapse; width: 100%; max-width: 600px;">
        <tr style="background-color: #f2f2f2;">
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Finding ID</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{nc_ofi.id}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Type</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{nc_ofi.type}</td>
        </tr>
        <tr style="background-color: #f2f2f2;">
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Severity</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;"><span style="color: {'red' if nc_ofi.severity == 'Critical' else 'orange' if nc_ofi.severity == 'Major' else 'blue'};">{nc_ofi.severity}</span></td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Clause</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{nc_ofi.clause_no}</td>
        </tr>
        <tr style="background-color: #f2f2f2;">
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Description</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{nc_ofi.description}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Due Date</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{nc_ofi.due_date.strftime('%Y-%m-%d') if nc_ofi.due_date else 'Not set'}</td>
        </tr>
        <tr style="background-color: #f2f2f2;">
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Status</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{nc_ofi.status}</td>
        </tr>
    </table>

    <p>Please review and take necessary action.</p>

    <hr>
    <p style="color: #666; font-size: 12px;">Audit Pro Enterprise</p>
</body>
</html>
"""

    return send_email(assignee.email, subject, body, html_body)


def send_overdue_notification(nc_ofi, assignee):
    """
    Send email notification for overdue NC/OFI

    Args:
        nc_ofi: NCOFI model instance
        assignee: User model instance
    """
    subject = f"[Audit Pro] OVERDUE: {nc_ofi.type} - {nc_ofi.severity} - {nc_ofi.clause_no}"

    days_overdue = abs(nc_ofi.days_until_due) if nc_ofi.days_until_due else 0

    body = f"""
URGENT: Overdue Finding

Hello {assignee.full_name},

The following {nc_ofi.type} finding is OVERDUE by {days_overdue} days:

Finding ID: {nc_ofi.id}
Type: {nc_ofi.type}
Severity: {nc_ofi.severity}
Clause: {nc_ofi.clause_no}
Due Date: {nc_ofi.due_date.strftime('%Y-%m-%d')}
Days Overdue: {days_overdue}
Current Status: {nc_ofi.status}

Please take immediate action to address this finding.

---
Audit Pro Enterprise
"""

    html_body = f"""
<html>
<body>
    <div style="background-color: #ffcccc; padding: 10px; border-left: 4px solid red;">
        <h2 style="color: red; margin: 0;">⚠️ URGENT: Overdue Finding</h2>
    </div>

    <p>Hello {assignee.full_name},</p>

    <p>The following <strong>{nc_ofi.type}</strong> finding is <strong style="color: red;">OVERDUE</strong> by <strong>{days_overdue} days</strong>:</p>

    <table style="border-collapse: collapse; width: 100%; max-width: 600px;">
        <tr style="background-color: #f2f2f2;">
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Finding ID</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{nc_ofi.id}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Type</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{nc_ofi.type}</td>
        </tr>
        <tr style="background-color: #f2f2f2;">
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Severity</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;"><span style="color: red; font-weight: bold;">{nc_ofi.severity}</span></td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Clause</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{nc_ofi.clause_no}</td>
        </tr>
        <tr style="background-color: #f2f2f2;">
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Due Date</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{nc_ofi.due_date.strftime('%Y-%m-%d')}</td>
        </tr>
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Days Overdue</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;"><span style="color: red; font-weight: bold;">{days_overdue}</span></td>
        </tr>
        <tr style="background-color: #f2f2f2;">
            <td style="padding: 8px; border: 1px solid #ddd;"><strong>Current Status</strong></td>
            <td style="padding: 8px; border: 1px solid #ddd;">{nc_ofi.status}</td>
        </tr>
    </table>

    <p style="color: red; font-weight: bold;">Please take immediate action to address this finding.</p>

    <hr>
    <p style="color: #666; font-size: 12px;">Audit Pro Enterprise</p>
</body>
</html>
"""

    return send_email(assignee.email, subject, body, html_body)
