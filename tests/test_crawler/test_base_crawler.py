import unittest
from unittest.mock import Mock

from src.crawler.base_crawler import BaseCrawler


class TestBaseCrawler(unittest.TestCase):
    def setUp(self):
        self.start_url = 'http://example.com'
        self.crawl_id = 'test_crawl'
        self.crawler = BaseCrawler(self.start_url, self.crawl_id)

    def test_check_visited(self):
        # Test the check_visited method
        url = 'http://example.com'
        self.crawler.visited_urls.add(url)
        result = self.crawler.check_visited(url)
        self.assertTrue(result)

    def test_check_rules_success(self):
        url = 'http://example.com/page1'

        mock_rule1 = Mock()
        mock_rule2 = Mock()

        mock_rule1.check.return_value = True
        mock_rule2.check.return_value = True

        self.crawler.rules = [mock_rule1, mock_rule2]

        result = self.crawler.check_rules(url)

        # Assertions
        self.assertTrue(result)
        mock_rule1.check.assert_called_with(url)
        mock_rule2.check.assert_called_with(url)

    def test_check_rules_failure(self):
        url = 'http://example.com/page1'

        mock_rule1 = Mock()
        mock_rule2 = Mock()

        mock_rule1.check.return_value = True
        mock_rule2.check.return_value = False

        self.crawler.rules = [mock_rule1, mock_rule2]

        result = self.crawler.check_rules(url)

        # Assertions
        self.assertFalse(result)
        mock_rule1.check.assert_called_with(url)
        mock_rule2.check.assert_called_with(url)

    def test_extract_links(self):
        page_content = '<html><body><a href="http://example.com/page1">Page 1</a><a href="http://example.com/page2">Page 2</a></body></html>'
        expected_links = ['http://example.com/page1', 'http://example.com/page2']

        response = Mock()
        response.text = page_content
        links = [*self.crawler.extract_links(response)]

        # Assertions
        self.assertEqual(links, expected_links)

    def test_extract_links_empty_content(self):
        response = Mock()
        response.text = ''
        expected_links = []

        links = [*self.crawler.extract_links(response)]

        # Assertions
        self.assertEqual(links, expected_links)

    def test_bad_html(self):
        response = Mock()
        response.text = '<html><body>Hello, World!</html>'
        expected_links = []

        links = [*self.crawler.extract_links(response)]

        # Assertions
        self.assertEqual(links, expected_links)


if __name__ == '__main__':
    unittest.main()
