import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from data.storage import Storage

load_dotenv(".env", verbose=True)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
DATA_FILE = "data/items_notified.json"
TEMPLATE_FILE = "data/items_notified_template.json"


class Notifier:
    def __init__(self, new_items):
        """
        new_items: dict with the scraped items that had not been scraped (and notified) before.
        """
        self.storage = Storage(DATA_FILE, TEMPLATE_FILE)
        self.new_items = new_items if new_items else {}

    def send_slack_notification(self, item):
        """Send notification to Slack."""
        print(f"ℹ️  Sending Slack notification for {item['title']}...")
        message = f"🔹 *{item['title']}*\n💰 {item['price']}\n🔗 <{item['link']}>"
        payload = {"text": message}

        print(f"Slack webhook URL: {SLACK_WEBHOOK_URL}")
        try:
            response = requests.post(SLACK_WEBHOOK_URL, json=payload)
            status = "success" if response.status_code == 200 else "failed"
            error_message = None if response.status_code == 200 else response.text
        except requests.exceptions.RequestException as e:
            status, error_message = "failed", str(e)

        return status, error_message

    def process_notifications(self):
        """
        Check and send notifications for unsent items.
        """
        print("🚀 Processing notifications...")
        print(f"Found {len(self.new_items)} new items.")

        print(self.new_items)
        items = self.new_items
        timestamp = datetime.now().isoformat()

        for item in self.new_items:
            status, error_message = self.send_slack_notification(item)

            # Update notification status
            item = {
                "sent": True,
                "timestamp": timestamp,
                "error": error_message,
                "status": status,
            }
            print(item)

        # with open(DATA_FILE, "w") as file:
        #     json.dump(items, file, indent=4)

        print("✅ Notification processing completed.")
