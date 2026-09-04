import random
import time
from datetime import datetime
from urllib.parse import urljoin

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
            # Identifies your browser/OS (prevents blocking).
            "User-Agent": get_random_user_agent(),
            # Tells the site where you came from (google.com in this case).
            "Referer": "https://www.google.com",
            # Tells the site which languages you accept.
            "Accept-Language": "en-GB,en;q=0.9",
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to fetch the webpage: {url}. Error: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        self.log_fetch_diagnostics(url, response, soup)

        items = self.extract_items(soup)

        print(f"Found {len(items)} items on {url}")

        return items

    def log_fetch_diagnostics(self, url, response, soup):
        title = soup.title.get_text(strip=True) if soup.title else "N/A"
        print(
            f"🌐 Fetch diagnostics: status={response.status_code}, final_url={response.url}, bytes={len(response.text)}, title={title}"
        )

        protection_markers = [
            "cloudflare",
            "captcha",
            "just a moment",
            "access denied",
            "verify you are a human",
            "cf_chl",
            "challenge-platform",
        ]
        response_text = response.text.lower()
        found_markers = [marker for marker in protection_markers if marker in response_text]
        if found_markers:
            print(f"⚠️ Potential anti-bot markers detected: {', '.join(found_markers)}")

    def extract_items(self, soup):
        selector_strategies = [
            ("div.detail", "a", "span.money"),
            ("li.grid__item", "a.full-unstyled-link, a", "span.price-item, span.money"),
            ("div.grid-product__content", "a.grid-product__title, a", "span.money, span.price-item"),
        ]

        extracted_items = {}
        for container_selector, title_selector, price_selector in selector_strategies:
            for container in soup.select(container_selector):
                title_tag = container.select_one(title_selector)
                price_tag = container.select_one(price_selector)

                if not title_tag or not price_tag:
                    continue

                title = title_tag.get_text(strip=True)
                href = title_tag.get("href")
                price = price_tag.get_text(strip=True).replace("\u00a3", "")

                if not title or not href or not self.filter_words(title):
                    continue

                link = urljoin("https://www.savvyrow.co.uk", href)
                extracted_items[title] = {"title": title, "link": link, "price": price}

        if not extracted_items:
            print("⚠️ No items extracted using known selectors.")

        return list(extracted_items.values())

    def filter_words(self, title):
        """
        Filter sizes 34, 35, 36, 37, 38, 39, 40 in title
        """
        sizes = [
            "shoe",
            "30",
            "31",
            "32",
            "33",
            "34",
            "35",
            "36",
            "37",
            "38",
            "39",
            "40",
        ]
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
