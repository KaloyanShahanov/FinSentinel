import smtplib
from email.mime.text import MIMEText
import logging

# Configure logging to output to console with DEBUG level
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

def send_test_email():
    sender = "kaloqnshahanov@abv.bg"
    recipient = "kaloqnshahanov@abv.bg"
    subject = "Test Email from Python"
    body = "This is a test email to verify ABV SMTP settings."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        logging.info("Connecting to ABV SMTP server...")
        with smtplib.SMTP_SSL("smtp.abv.bg", 465) as server:
            logging.info("Logging in...")
            server.login(sender, "kaloqn123")  
            logging.info("Sending email...")
            server.send_message(msg)
            logging.info("Test email sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send test email: {e}")

if __name__ == "__main__":
    send_test_email()
