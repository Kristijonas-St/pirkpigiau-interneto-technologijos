import unittest
from scraping_feature.scraping_feature import ScrapingRequest
from speech_response_feature.speech_response import say_formatted_response


def perform_scraping(item_name, shops):
    data = []
    results = dict()
    index = 0
    for shop in shops:
        request = ScrapingRequest(shop, item_name)
        data.append(request.scrape_price())
        if data[index]:
            message = f"{shop.upper()}: Pigiausias variantas: [{data[index].item_name}]({data[index].item_url}) už "
            price = float(data[index].cheapest_item)
            results[message] = price
            say_formatted_response(data[index].item_name, shop, data[index].cheapest_item)
        else:
            message = f"{shop.upper()}: Prekė {item_name} nerasta."
            price = float('inf')
            results[message] = price
        index += 1
    return sorted(results.items(), key=lambda x: x[1])


class TestManualInputSearch(unittest.TestCase):
    def setUp(self):
        self.shops = ["Rimi", "Maxima", "IKI"]
        self.item_name = "Agurkas"

    def test_perform_scraping_with_valid_item(self):
        results = perform_scraping(self.item_name, self.shops)
        self.assertIsInstance(results, list)
        for result in results:
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            self.assertIsInstance(result[0], str)
            self.assertIsInstance(result[1], float)

if __name__ == "__main__":
    unittest.main()