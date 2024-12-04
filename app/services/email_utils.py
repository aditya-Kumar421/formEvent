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
    <!DOCTYPE html>
<html lang="en">
<body>
    <div class="container">
        <div class="header">
            <h1>Registration Successful!</h1>
        </div>
        <div class="content">
            <p>Congratulations, <span class="highlight">{name}</span>! Your registration for <strong>DevClash</strong> has been successfully completed. 🎉</p>
            <p><em>“Unleash your creativity, solve challenges, and make your mark in the world of development!” ⭐</em></p>
            <p>Get ready for two exciting rounds:</p>
            <ul>
                <li><strong>Elimination Round:</strong> Test your technical knowledge and compete for a spot in the top 10 teams.</li>
                <li><strong>Development Round:</strong> Build app or web pages based on provided designs.</li>
            </ul>
            <p><span class="highlight">🌟 Grand Prizes:</span> Cash prizes for the top two teams in both app and web categories!</p>
            <p><strong>📅 Date:</strong> 6th December 2024<br>
               <strong>⏲️ Time:</strong> 4pm onwards<br>
               <strong>📍 Venue:</strong> IT labs, 3rd Floor, CSIT</p>
            
            <p>If you have any questions, feel free to contact:</p>
            <ul>
                <li>Prakhar Srivastava: 8707074420</li>
                <li>Manoj Samantha</li>
            </ul>
        </div>
        <div class="footer">
            &copy; 2024 DevClash | Organized by Cloud Computing Cell
        </div>
    </div>
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
