from notifier.notifier import Notifier
from scraper.scraper import Scraper

if __name__ == "__main__":
    scraper = Scraper()
    new_items = scraper.check_new_items()
    if new_items:
        notifier = Notifier(new_items)
        notifier.process_notifications()
