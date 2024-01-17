import unittest
from unittest.mock import Mock, patch, ANY

from src.crawler.html_crawler import HTMLCrawler
from src.infra.base_storage import BaseStorage
from common.enums import CrawlStatus


class TestHTMLCrawler(unittest.TestCase):
    def test_crawl_success(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value.text = '<html><body>Hello, World!</body></html>'
            mock_get.return_value.raise_for_status.return_value = None

            mock_storage = Mock(spec=BaseStorage)

            crawler = HTMLCrawler(start_url='http://example.com', crawl_id='test_crawl', feed_storage=mock_storage)

            result = crawler.crawl()

            # Assertions
            expected_result = {
                'crawl_id': 'test_crawl',
                'directory': mock_storage.save_crawl_request(),
                'status': CrawlStatus.COMPLETE
            }
            self.assertEqual(result, expected_result)
            mock_storage.save_html.assert_called_once_with('test_crawl', 'http://example.com',
                                                           '<html><body>Hello, World!</body></html>',
                                                           encoding=ANY)

    def test_crawl_failure(self):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("Mocked exception")

            mock_storage = Mock(spec=BaseStorage)

            crawler = HTMLCrawler(start_url='http://example.com', crawl_id='test_crawl', feed_storage=mock_storage)

            result = crawler.crawl()

            # Assertions
            expected_result = {
                'crawl_id': 'test_crawl',
                'directory': mock_storage.save_crawl_request(),
                'status': CrawlStatus.ERROR,
                'error': 'Mocked exception'
            }
            self.assertEqual(result, expected_result)
            mock_storage.save_html.assert_not_called()


if __name__ == '__main__':
    unittest.main()
