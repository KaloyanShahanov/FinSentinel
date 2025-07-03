# Slack alerts
import requests

def send_slack_alert(coin_name, price):
    webhook_url = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    message = {
        "text": f":rotating_light: {coin_name} price dropped by 5%! Current: ${price}"
    }
    try:
        response = requests.post(webhook_url, json=message)
        if response.status_code != 200:
            print(f"Slack error for {coin_name}:", response.text)
    except Exception as e:
        print(f"Slack exception for {coin_name}:", e)


# Abv emails alerts
import smtplib
from email.mime.text import MIMEText

def send_email_alert(coin_name, price):
    sender = "kaloqnshahanov@abv.bg" # the sender is the person who owns the web application
    recipient = "kaloqnshahanov@abv.bg"  # who receives the alert
    subject = f"{coin_name} Price Alert"
    body = f"{coin_name} price alert! Current price: ${price}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.abv.bg", 465) as server:
            server.login(sender, "abv password") # replace with abv sender email password
            server.send_message(msg)
            print(f"Email alert sent for {coin_name}.")
    except Exception as e:
        print(f"Email alert error for {coin_name}:", e)

# Send test alert to verify email and Slack notifications
import smtplib
from email.mime.text import MIMEText
import logging

# Configure logging to output to console with DEBUG level
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

# def send_test_email():
#    sender = "kaloqnshahanov@abv.bg"
#    recipient = "kaloqnshahanov@abv.bg"
#    subject = "Test Email from Python"
#    body = "This is a test email to verify ABV SMTP settings."

#    msg = MIMEText(body)
#    msg['Subject'] = subject
#    msg['From'] = sender
#   msg['To'] = recipient

#    try:
#       logging.info("Connecting to ABV SMTP server...")
#       with smtplib.SMTP_SSL("smtp.abv.bg", 465) as server:
#            logging.info("Logging in...")
#            server.login(sender, "abv email password") 
#            logging.info("Sending email...")
#            server.send_message(msg)
#           logging.info("Test email sent successfully.")
#   except Exception as e:
#        logging.error(f"Failed to send test email: {e}")

# if __name__ == "__main__":
#    send_test_email()
