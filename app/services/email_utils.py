from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi import HTTPException
import smtplib
from app.config.settings import settings

async def send_email(email: str, name: str):
    """
    Sends a confirmation email with HTML content.
    """
    # Create HTML content for the email
    message = f"""
    <html>
    <body>
        <p>Dear {name},</p>
        <p>Thank you for registering on our platform. Here are your details:</p>
        <ul>
            <li><b>Name:</b> {name}</li>
            <li><b>Email:</b> {email}</li>
        </ul>
        <p>Best regards,<br>Your Team</p>
    </body>
    </html>
    """
    smtp_host = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_user = settings.smtp_user
    smtp_password = settings.smtp_password
    

    # Create the email message object
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = email
    msg['Subject'] = "Registration Successful"
    
    # Attach the HTML content to the email
    msg.attach(MIMEText(message, 'html'))

    try:
        # Sending email asynchronously
        with smtplib.SMTP(host=smtp_host, port=smtp_port) as smtp:
            smtp.starttls()  # Start TLS encryption
            smtp.login(smtp_user, smtp_password)  # Log in to the SMTP server
            smtp.send_message(msg)  # Send the email

        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")
