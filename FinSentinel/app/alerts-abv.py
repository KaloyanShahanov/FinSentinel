import smtplib
from email.mime.text import MIMEText

def send_email_alert(price):
    sender = "kaloqnshahanov@abv.bg" # the sender is the person who owns the web application
    recipient = "kaloqnshahanov@abv.bg"  # who receives the alert
    subject = "Bitcoin Price Drop Alert"
    body = f"Bitcoin price has dropped! Current price: ${price}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP("smtp.abv.bg", 587) as server:
            server.starttls()
            server.login("kaloqnshahanov@abv.bg", "kaloqn123")
            server.send_message(msg)
            print("Email alert sent.")
    except Exception as e:
        print("Email alert error:", e)
