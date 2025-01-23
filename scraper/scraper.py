import random
import time

import requests
from bs4 import BeautifulSoup

from scraper.config import URLS, get_random_user_agent
from scraper.storage import Storage


class Scraper:
    def __init__(self):
        self.URLS = URLS
        self.storage = Storage()

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
            if title_tag and price_tag:
                title = title_tag.get_text(strip=True)
                link = "https://www.savvyrow.co.uk" + title_tag["href"]
                price = price_tag.get_text(strip=True).replace("\u00a3", "")
                items.append({"title": title, "link": link, "price": price})

        print(f"Found {len(items)} items on {url}")

        return items

    def check_new_items(self):
        """Compare fetched items with stored items and update list with timestamps."""
        new_items = []

        for url in self.URLS:
            time.sleep(random.uniform(2, 5))  # Random delay to avoid detection
            fetched_items = self.fetch_items(url)

            if not self.storage.existing_items:
                print("No existing items")
                new_items.extend(fetched_items)
            else:
                for item in fetched_items:
                    print("get back fetched item", fetched_items)
                    existing_titles = self.storage.existing_items.keys()
                    if item["title"] not in existing_titles:
                        new_items.append(item)

        if new_items:
            print(f"{len(new_items)} items are new, saving them")
            self.storage.save_items(new_items)

        return new_items
