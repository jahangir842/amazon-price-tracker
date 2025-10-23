import requests
import os

def send_notification(product_name, url, price):
    """
    Sends a notification (example via Slack) for a price alert.
    """
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")  # load from environment variable
    if not webhook_url:
        print("Slack webhook not set in environment. Skipping notification.")
        return

    message = f"Price Alert! {product_name} is now ${price}\n{url}"
    try:
        response = requests.post(webhook_url, json={"text": message})
        if response.status_code != 200:
            print(f"Failed to send notification: {response.text}")
    except Exception as e:
        print(f"Error sending notification: {e}")
