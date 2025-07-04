#Slack alerts
import requests

def send_slack_alert(coin_name, price_binance, price_bitfinex, percent_diff):
    webhook_url = "https://hooks.slack.com/services/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"
    emoji = ":rotating_light:"  # Alert emoji
    
    message = {
        "text": (
            f"{emoji} {coin_name} price difference alert!\n"
            f"Binance: EUR {price_binance:.6f}\n"
            f"Bitfinex: EUR {price_bitfinex:.6f}\n"
            f"Difference: {percent_diff:.8f}%"
        )
    }
    try:
        response = requests.post(webhook_url, json=message)
        if response.status_code != 200:
            print(f"Slack error for {coin_name}:", response.text)
    except Exception as e:
        print(f"Slack exception for {coin_name}:", e)


#
#ABV email alerts
#import smtplib
#from email.mime.text import MIMEText

#def send_email_alert(coin_name, price):
    #sender = "kaloqnshahanov@abv.bg"  # sender email address
    #recipient = "kaloqnshahanov@abv.bg"  # recipient email address
    #subject = f"{coin_name} Price Alert"
   # body = f"{coin_name} price alert! Current price: EUR {price}"

   # msg = MIMEText(body)
  #  msg['Subject'] = subject
   # msg['From'] = sender
   # msg['To'] = recipient

   # try:
    #    with smtplib.SMTP_SSL("smtp.abv.bg", 465) as server:
    #        server.login(sender, "abv password")  # replace with your ABV email password
    #        server.send_message(msg)
    #        print(f"Email alert sent for {coin_name}.")
   # except Exception as e:
    #    print(f"Email alert error for {coin_name}:", e)


# The following test alert code is commented out and can be enabled if needed
# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

# def send_test_email():
#     sender = "kaloqnshahanov@abv.bg"
#     recipient = "kaloqnshahanov@abv.bg"
#     subject = "Test Email from Python"
#     body = "This is a test email to verify ABV SMTP settings."
#
#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = sender
#     msg['To'] = recipient
#
#     try:
#         logging.info("Connecting to ABV SMTP server...")
#         with smtplib.SMTP_SSL("smtp.abv.bg", 465) as server:
#             logging.info("Logging in...")
#             server.login(sender, "abv email password")
#             logging.info("Sending email...")
#             server.send_message(msg)
#             logging.info("Test email sent successfully.")
#     except Exception as e:
#         logging.error(f"Failed to send test email: {e}")
#
# if __name__ == "__main__":
#     send_test_email()
