import json
import os


class Storage:
    def __init__(self, data_file, template_file):
        self.existing_items = {}
        self.template = {}
        self.DATA_FILE = data_file
        self.TEMPLATE_FILE = template_file
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

        self.existing_items.update(new_items)

        with open(self.DATA_FILE, "w") as file:
            json.dump(self.existing_items, file, indent=4)
