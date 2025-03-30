import pytest
from scraping_feature.scraping_feature import ScrapingRequest

@pytest.mark.parametrize("item_to_search", ["bananai", "pomidorai", "agurkas"])
def test_scraping_rimi_item(item_to_search):
    """Test if the returned item_name contains the searched item in Rimi."""
    shop_name = "Rimi"

    request = ScrapingRequest(shop_name, item_to_search)
    data = request.scrape_price()

    assert data, f"Scraping returned None, but expected a result for {item_to_search}."
    assert hasattr(data, "item_name"), f"Scraping result has no 'item_name' for {item_to_search}."
    assert item_to_search in data.item_name.lower(), f"Expected '{item_to_search}' in '{data.item_name}'"
