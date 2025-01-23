import random
import time

from scraper.scraper import Scraper

if __name__ == "__main__":
    scraper = Scraper()
    new_items = scraper.check_new_items()
