import json
import os
from datetime import datetime

DATA_FILE = "data/items.json"

class Storage:
    def __init__(self):
        self.load_existing_items()

    def load_existing_items(self):
        """Load previously stored items from JSON file."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                try:
                    self.existing_items = json.load(file)
                except json.JSONDecodeError:
                    self.existing_items = {}
        else:
            self.existing_items = {}

    def save_items(self):
        """Save items to JSON file."""
        with open(DATA_FILE, "w") as file:
            json.dump(self.existing_items, file, indent=4)

    def add_item(self, item):
        """Add a new item with a timestamp."""
        timestamp = datetime.now().isoformat()
        if item not in self.existing_items:
            self.existing_items[item] = timestamp
            self.save_items()
            return True  # Indicates new item found
        return False  # Item already exists
