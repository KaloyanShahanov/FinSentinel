import requests

def send_slack_alert(price):
    webhook_url = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    message = {
        "text": f":rotating_light: Bitcoin price dropped! Current: ${price}"
    }
    try:
        response = requests.post(webhook_url, json=message)
        if response.status_code != 200:
            print("Slack error:", response.text)
    except Exception as e:
        print("Slack exception:", e)
