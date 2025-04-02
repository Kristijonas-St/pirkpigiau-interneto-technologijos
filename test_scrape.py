from scraping.scrapers.rimi_scraper import RimiScraper

item_name = 'pomidorai'

if __name__ == "__main__":
    scraper = RimiScraper(item_name)
    result = scraper.scrape()
    
    if result and result.product_is_found:
        print(f"{result.item_name}: {result.cheapest_item} EUR")
    else:
        print(f"No results found for {item_name}.")
