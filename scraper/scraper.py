import requests
from bs4 import BeautifulSoup
import time
import random
from scraper.storage import Storage
from scraper.config import URLS, get_random_user_agent

class Scraper:
    def __init__(self):
        self.storage = Storage()

    def fetch_items(self, url):
        """Scrape website for items."""
        headers = {"User-Agent": get_random_user_agent()}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch the webpage: {url}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='grid-product__title')

        return [item.get_text(strip=True) for item in items]

    def check_new_items(self):
        """Compare fetched items with stored items and update list."""
        new_items = []

        for url in URLS:
            time.sleep(random.uniform(2, 5))  # Random delay to avoid detection
            fetched_items = self.fetch_items(url)

            for item in fetched_items:
                if self.storage.add_item(item):
                    new_items.append(item)

        return new_items
