import requests
from bs4 import BeautifulSoup

from .scrapers.iki_scraper import IkiScraper
from .scrapers.maxima_scraper import MaximaScraper
from .scrapers.rimi_scraper import RimiScraper




class ScrapingRequest:
    def __init__(self, shop_name, item):
        self.shop_name = shop_name
        self.item = item
        self.item_url = None
        self.cheapest_item = None
        self.message = None
        self.item_name = None

    def scrape_price(self):
        match self.shop_name:
            case "Maxima":
                result = MaximaScraper()
                self.item_name, self.cheapest_item, self.item_url, self.message = result.scrape(self.item)
                if self.item_name and self.cheapest_item and self.item_url and self.message:
                    return self

                return None
            case "IKI":
                result = IkiScraper()
                self.item_name, self.cheapest_item, self.item_url, self.message = result.scrape(self.item)
                if self.item_name and self.cheapest_item and self.item_url and self.message:
                    return self

                return None
            case "Rimi":
                result = RimiScraper()
                self.item_name, self.cheapest_item, self.item_url, self.message = result.scrape(self.item)
                if self.item_name and self.cheapest_item and self.item_url and self.message:
                    return self
                
                return None
            case _:
                print("Unknown error")



