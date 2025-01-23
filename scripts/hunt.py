from scraper.scraper import Scraper

if __name__ == "__main__":
    scraper = Scraper()
    new_items = scraper.check_new_items()

    # if new_items:
    #     print("New items found:", new_items)
    # else:
    #     print("No new items found.")
