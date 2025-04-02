from scraping.scrapers.rimi_scraper import RimiScraper
from scraping.scrapers.maxima_scraper import MaximaScraper
from scraping.scrapers.iki_scraper import IkiScraper


item_name = 'Pomidorai'

if __name__ == "__main__":
    
    scraper = RimiScraper(item_name)
    result = scraper.scrape()
    if result and result.product_is_found:
        print(f"RIMI: {result.item_name}: {result.cheapest_item} EUR")
    else:
        print(f"No results found for {item_name}.")
    
    scraper = MaximaScraper(item_name)
    result = scraper.scrape()
    if result and result.product_is_found:
        print(f"Maxima: {result.item_name}: {result.cheapest_item} EUR")
    else:
        print(f"No results found for {item_name}.")

    scraper = IkiScraper(item_name)
    result = scraper.scrape()
    if result and result.product_is_found:
        print(f"IKI: {result.item_name}: {result.cheapest_item} EUR")
    else:
        print(f"No results found for {item_name}.")



