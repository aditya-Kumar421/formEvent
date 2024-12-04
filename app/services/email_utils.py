from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
import smtplib
from app.config.settings import settings
from pathlib import Path



async def send_email(email: str, name: str):
    """
    Sends a confirmation email with HTML content.
    """
    # html_path = Path("templates/email_template.html")
    html_path = Path(__file__).parent / "templates/email_template.html"
    html_content = html_path.read_text(encoding="utf-8")
    html_content = html_content.replace("{{ name }}", name)

    smtp_host = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_user = settings.smtp_user
    smtp_password = settings.smtp_password
    

    # Create the email message object
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email
    msg['Subject'] = "Dev Clash Team Registration Confirmed 🚀"
    
    # Attach the HTML content to the email
    msg.attach(MIMEText(html_content, 'html'))

    try:
        # Sending email asynchronously
        with smtplib.SMTP(host=smtp_host, port=smtp_port) as smtp:
            smtp.starttls()  # Start TLS encryption
            smtp.login(smtp_user, smtp_password)  # Log in to the SMTP server
            smtp.send_message(msg)  # Send the email

        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")
