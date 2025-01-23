import json
import os
from datetime import datetime


class Storage:
    def __init__(self):
        self.DATA_FILE = "data/items.json"
        self.TEMPLATE_FILE = "data/item_template.json"
        self.existing_items = {}
        self.template = {}
        self.load_existing_items()
        self.load_template()

    def load_existing_items(self):
        """Load previously stored items from JSON file."""
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r") as file:
                try:
                    self.existing_items = json.load(file)
                except json.JSONDecodeError:
                    self.existing_items = {}
        else:
            self.existing_items = {}

    def load_template(self):
        """Load JSON template file to structure new items."""
        if os.path.exists(self.TEMPLATE_FILE):
            try:
                with open(self.TEMPLATE_FILE, "r") as file:
                    self.template = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {self.TEMPLATE_FILE}: {e}")
                self.template = {}
        else:
            print(f"Template file {self.TEMPLATE_FILE} does not exist.")
            self.template = {}

    def save_items(self, new_items):
        """Save new items to JSON file after processing."""
        processed_items = self.preprocess_new_items(new_items)

        self.existing_items.update(processed_items)  # Merge new items with existing

        with open(self.DATA_FILE, "w") as file:
            json.dump(self.existing_items, file, indent=4)

    def preprocess_new_items(self, new_items):
        """Process new items by using the template and updating values."""
        timestamp = datetime.now().isoformat()
        processed_items = {}

        for item in new_items:
            item_data = self.template.copy()  # Load structure from template
            item_data.update(
                {
                    "title": item["title"],
                    "link": item["link"],
                    "price": item["price"],
                    "timestamp processed": timestamp,
                }
            )
            processed_items[item["title"]] = item_data

        return processed_items
