import json
import os
from datetime import datetime

import requests

from scraper.storage import Storage

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


class Notifier:
    def __init__(self):
        self.storage = Storage()

    def get_notifications_to_send(self):
        """
        Parses the existing items and returns the ones where notified is False.
        """


    def send_slack_notification(self, item):
        """Send notification to Slack."""
        message = f"🔹 *{item['title']}*\n💰 {item['price']}\n🔗 <{item['link']}>"
        payload = {"text": message}

        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        status = "success" if response.status_code == 200 else "failed"
        error_message = None if response.status_code == 200 else response.text

        return status, error_message

    def process_notifications(self):
        """Check and send notifications for unsent items."""
        items = self.storage.existing_items
        timestamp = datetime.now().isoformat()

        for title, data in items.items():
            if "notification" not in data or not data["notification"].get(
                "sent", False
            ):
                status, error_message = self.send_slack_notification(data)

                # Update notification status
                data["notification"] = {
                    "sent": True,
                    "timestamp": timestamp,
                    "error": error_message,
                    "status": status,
                }

        with open(DATA_FILE, "w") as file:
            json.dump(items, file, indent=4)

        print("✅ Notification processing completed.")

    if __name__ == "__main__":
        process_notifications()
