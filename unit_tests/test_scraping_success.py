import pytest
from unittest.mock import patch, Mock
from scraping_feature.scrapers.iki_scraper import IkiScraper

FAKE_HTML = """
<html>
    <body>
        <div class="d-flex flex-column justify-content-between position-relative h-100">
            <p class="akcija_title w-100">Test Product</p>
            <div class="price_int">3</div>
            <span class="sub">99</span>
        </div>
    </body>
</html>
"""

@pytest.fixture
def scraper():
    return IkiScraper()

@patch("requests.get")
def test_scraping_success(mock_get, scraper):
    """Test if IkiScraper successfully extracts a product"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = FAKE_HTML
    mock_get.return_value = mock_response

    product_name, price, url, status = scraper.scrape("Test Product")

    assert status == "success"
    assert product_name is not None and product_name != ""
    assert price is not None and price != ""
