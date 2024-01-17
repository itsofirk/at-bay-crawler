import unittest
from unittest.mock import MagicMock, patch
from multiprocessing import Queue
from common.enums import CrawlStatus
from crawler.crawl_manager import CrawlManager
from crawler.base_crawler import BaseCrawler


class MockCrawler(BaseCrawler):
    def crawl(self):
        return {'status': CrawlStatus.COMPLETE, 'directory': 'test_dir'}


class TestCrawlManager(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()
        self.manager = CrawlManager(crawler_class=MockCrawler, queue=self.queue)

    def test_handle_crawl_result(self):
        result = {'status': CrawlStatus.COMPLETE, 'crawl_id': 'test_id', 'key1': 'value1', 'key2': 'value2'}
        with patch('crawler.crawl_manager.set_status') as mock_set_status:
            self.manager.handle_crawl_result(result)
            mock_set_status.assert_called_once_with('test_id', CrawlStatus.COMPLETE, key1='value1', key2='value2')

    def test_start_listening(self):
        with patch('crawler.crawl_manager.Pool', autospec=True) as mock_pool, \
                patch('crawler.crawl_manager.set_status') as mock_set_status:

            mock_pool.return_value.__enter__.return_value.apply_async = MagicMock()

            self.queue.get = MagicMock(side_effect=[
                {'start_url': 'url1', 'crawl_id': 'id1'},
                {'start_url': 'url2', 'crawl_id': 'id2'},
                {'start_url': 'url3', 'crawl_id': 'id3'},
            ])

            self.manager._validate_crawl_request = MagicMock(return_value=None)
            mock_crawler = MockCrawler(start_url=None, crawl_id=None)
            self.manager.crawler_class = MagicMock(return_value=mock_crawler)

            try:
                self.manager.start_listening()
            except StopIteration:
                pass  # a workaround for the infinite loop in start_listening

            # Assertions
            self.assertEqual(mock_set_status.call_count, 3)
            mock_pool.assert_called()
            apply_async = mock_pool.return_value.__enter__.return_value.apply_async
            self.assertEqual(apply_async.call_count, 3)
            expected_calls = [
                ((mock_crawler.crawl,), {'callback': self.manager.handle_crawl_result}),
                ((mock_crawler.crawl,), {'callback': self.manager.handle_crawl_result}),
                ((mock_crawler.crawl,), {'callback': self.manager.handle_crawl_result}),
            ]
            apply_async.assert_has_calls(expected_calls)


if __name__ == '__main__':
    unittest.main()
