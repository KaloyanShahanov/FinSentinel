import smtplib
from email.mime.text import MIMEText

def send_email_alert(price):
    sender = "kaloqnshahanov@abv.bg"
    recipient = "kaloqnshahanov@abv.bg"  # Can be the same or another
    subject = "Bitcoin Price Drop Alert"
    body = f"Bitcoin price has dropped! Current price: ${price}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP("smtp.abv.bg", 587) as server:
            server.starttls()
            server.login("testing email login", "testing password")
            server.send_message(msg)
            print("Email alert sent.")
    except Exception as e:
        print("Email alert error:", e)
