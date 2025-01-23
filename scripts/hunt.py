import random
import time

from scraper.scraper import Scraper

if __name__ == "__main__":
    scraper = Scraper()
    time.sleep(random.uniform(0, 120))
    new_items = scraper.check_new_items()
