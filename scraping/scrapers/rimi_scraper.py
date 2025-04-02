import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

from scraping.base_scraper.request import ScrapingRequest

headers = {'User-Agent': 'Mozilla/5.0'}

urls = [
    'https://www.rimi.lt/e-parduotuve/lt/produktai/vaisiai-darzoves-ir-geles/c/SH-15?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-15%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/augaliniai-produktai/c/SH-77?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-77%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/pieno-produktai-kiausiniai-ir-suris/c/SH-11?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-11%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/duonos-gaminiai-/c/SH-3?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-3%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/mesa-ir-zuvis-/c/SH-9?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-9%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/saldytas-maistas/c/SH-13?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-13%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/bakaleja/c/SH-2?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-2%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/rimi-konditerija-ir-kulinarija/c/SH-34?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-34%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/vaiku-ir-kudikiu-prekes/c/SH-7?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-7%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/saldumynai-ir-uzkandziai/c/SH-23?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-23%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/gerimai/c/SH-4?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-4%3AassortmentStatus%3AinAssortment',
    'https://www.rimi.lt/e-parduotuve/lt/produktai/alkoholiniai-ir-nealkoholiniai-gerimai/c/SH-1?currentPage=1&pageSize=20&query=%3Arelevance%3AallCategories%3ASH-1%3AassortmentStatus%3AinAssortment'
]

class RimiScraper(ScrapingRequest):
    def __init__(self, item_name):
        super().__init__("Rimi", item_name)
        
    def scrape(self):
        self.scrape_by_search(self.item_name + 'asdasdad')
        if self.product_is_found:
            return self

        print("Didn't find by QUERY, trying all known URLs...")

        self.scrape_by_urls(self.item_name)
        if self.product_is_found:
            return self
        
        return None
        
    def scrape_by_search(self, item):
        search_url = self.form_search_url(item)
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200:
            self.product_is_found = False
            return
        else:
            self.use_soup(response, item)

    def scrape_by_urls(self, item):
        for url in urls:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                continue

            self.use_soup(response, item)
            if self.product_is_found:
                break


    def form_search_url(self, item):
        return 'https://www.rimi.lt/e-parduotuve/lt/' + f'paieska?query={item}'
        
    def use_soup(self, response, item):
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('li', class_='product-grid__item')

        for product in products:
            if fuzz.partial_ratio(item.lower(), product.text.lower()) > 75:
                found_item_name = self.extract_item_name(product)
                euro, cents = self.extract_price(product)
                found_price = f"{euro}.{cents}"
                found_item_url = self.extract_hyperlink(product)

                self.product_is_found = True
                self.item_name = found_item_name
                self.cheapest_item = found_price
                self.item_url = found_item_url
                return
        self.product_is_found = False


    def extract_item_name(self, product):
        name_tag = product.find('a', class_='card__url js-gtm-eec-product-click')
        return name_tag.attrs['aria-label']

    def extract_price(self, product):
        price_tag = product.find('div', class_='price-tag card__price')
        euro = price_tag.find('span').text.strip()
        cents = price_tag.find('sup').text.strip()

        return euro, cents
    
    def extract_hyperlink(self, product):
        base_url = "https://www.rimi.lt"
        link_tag = product.find('a', class_='js-gtm-eec-product-click')
        if link_tag and 'href' in link_tag.attrs:
            return base_url + link_tag.attrs['href']    
        return None
    



