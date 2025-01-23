import random
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from data.storage import Storage
from notifier.notifier import Notifier
from scraper.config import URLS, get_random_user_agent


class Scraper:
    def __init__(self):
        self.URLS = URLS
        self.storage = Storage()
        self.notifier = Notifier()

    def fetch_items(self, url):
        """Scrape website for items."""
        headers = {
            "User-Agent": get_random_user_agent(),
            "Referer": "https://www.google.com",
            "Accept-Language": "en-US,en;q=0.9",
        }
        response = requests.get(url, headers=headers)
        print("First 1000 characters of response", response.text[:1000])

        if response.status_code != 200:
            print(f"Failed to fetch the webpage: {url}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        items = []

        for detail in soup.find_all("div", class_="detail"):
            title_tag = detail.find("a")
            price_tag = detail.find("span", class_="money")
            # Excludes items that are sold
            if title_tag and price_tag:
                title = title_tag.get_text(strip=True)
                link = "https://www.savvyrow.co.uk" + title_tag["href"]
                price = price_tag.get_text(strip=True).replace("\u00a3", "")
                if self.filter_size(title):
                    items.append({"title": title, "link": link, "price": price})

        print(f"Found {len(items)} items on {url}")

        return items

    def filter_size(self, title):
        """
        Filter sizes 34, 35, 36, 37, 38, 39, 40 in title
        """
        sizes = ["34", "35", "36", "37", "38", "39", "40"]
        return any(size in title for size in sizes)

    def check_new_items(self):
        """Compare fetched items with stored items and update list with timestamps."""
        new_items = []

        for url in self.URLS:
            time.sleep(random.uniform(2, 5))  # Random delay to avoid detection

            print(f"🔍 Checking for new items on {url}...")
            fetched_items = self.fetch_items(url)

            if not self.storage.existing_items:
                print("No existing items")
                new_items.extend(fetched_items)
            else:
                for item in fetched_items:
                    existing_titles = self.storage.existing_items.keys()
                    if item["title"] not in existing_titles:
                        new_items.append(item)

        if new_items:
            print(f"⭐️ {len(new_items)} items are new")
            new_items_processed = self.notify_and_process_items(new_items)
            self.storage.save_items(new_items_processed)
        else:
            print("No new items found")

        return new_items

    def notify_and_process_items(self, new_items):
        """Process new items by using the template and updating values."""
        timestamp = datetime.now().isoformat()
        processed_items = {}

        for item in new_items:
            notif_data = self.notifier.process_notifications(item)
            item_data = self.storage.template.copy()  # Load structure from template
            item_data.update(
                {
                    "title": item["title"],
                    "link": item["link"],
                    "price": item["price"],
                    "timestamp processed": timestamp,
                    "notification": notif_data,
                }
            )
            processed_items[item["title"]] = item_data

        return processed_items
