class ScrapingRequest:
    def __init__(self, shop_name, item_name):
        self.item_name = item_name
        self.shop_name = shop_name
        self.cheapest_item = None
        self.item_url = None
        self.product_is_found = False

    def scrape(self):
        raise NotImplementedError("Subclasses must implement scrape_price()")