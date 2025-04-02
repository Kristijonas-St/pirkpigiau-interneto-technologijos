import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

headers = {'User-Agent': 'Mozilla/5.0'}

url = "https://www.maxima.lt/pasiulymai"


class MaximaScraper:
    def scrape(self, item):
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None, None, None, None

        soup = BeautifulSoup(response.text, 'html.parser')
        if self.get_cheapest_product(item, soup):
            product_name, price = self.get_cheapest_product(item, soup)
            return product_name, price, url, 'success'

        return None, None, None, None

    def extract_containers_of_products_w_pricetags(self, soup):
        product_containers = soup.find_all('div', class_='card card-small is-pointer h-100')
        product_containers_w_pricetags = []

        for product_container in product_containers:
            if product_container.find('div', class_='bg-primary text-white h-100 rounded-end-1'):
                product_containers_w_pricetags.append(product_container)

        return product_containers_w_pricetags
    def extract_product_name(self, product_container):
        product_element = product_container.find('h4', class_='mt-4 text-truncate text-truncate--2')
        product_name = product_element.text.strip().lower()
        return product_name

    def extract_product_price(self, product_container):
        price_whole_element = product_container.find('div', class_='my-auto price-eur text-end')
        price_decimal_element = product_container.find('span', class_='price-cents')

        price_whole = price_whole_element.text.strip()
        price_decimal = price_decimal_element.text.strip()

        price = f"{price_whole}.{price_decimal}"
        return price

    def get_maxima_product_list(self, product_containers):
        mapping = dict()
        for product_container in product_containers:
            product_name = self.extract_product_name(product_container)
            price = self.extract_product_price(product_container)
            mapping[product_name] = price

        return mapping

    def find_matching_products(self, item, mapping):
        found_items = []
        for product_name in mapping:
            if fuzz.partial_ratio(item.lower(), product_name) > 75:
                found_items.append((product_name, mapping[product_name]))

        if not found_items:
            return None

        return found_items

    def get_cheapest_product(self, item, soup):
        product_containers = self.extract_containers_of_products_w_pricetags(soup)
        mapping = self.get_maxima_product_list(product_containers)
        found_items = self.find_matching_products(item, mapping)
        if not found_items:
            return None
        found_items.sort(key=lambda x: float(x[1]))
        return found_items[0][0], found_items[0][1]
