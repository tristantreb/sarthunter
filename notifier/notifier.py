import os
from datetime import datetime

import requests
from dotenv import load_dotenv


class Notifier:
    def __init__(self):
        """
        new_items: dict with the scraped items that had not been scraped (and notified) before.
        """
        load_dotenv(".env", verbose=True)
        self.SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

    def send_slack_notification(self, item):
        """Send notification to Slack."""
        print(f"ℹ️  Sending Slack notification for {item['title']}...")
        message = f"⭐️ *{item['title']}*\n💰 {item['price']}\n🔗 <{item['link']}>"
        payload = {"text": message}

        try:
            response = requests.post(self.SLACK_WEBHOOK_URL, json=payload)
            status = "success" if response.status_code == 200 else "failed"
            error_message = None if response.status_code == 200 else response.text
        except requests.exceptions.RequestException as e:
            status, error_message = "failed", str(e)

        return status, error_message

    def process_notifications(self, item):
        """
        Check and send notifications for unsent items.
        """
        print(f"🚀 Processing notifications for item {item['title']}...")
        status, error_message = self.send_slack_notification(item)

        # Update notification status
        notification_data = {
            "sent": True,
            "timestamp": datetime.now().isoformat(),
            "error": error_message,
            "status": status,
        }

        return notification_data
