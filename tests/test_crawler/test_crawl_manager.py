import unittest
from unittest.mock import Mock, patch
from multiprocessing import Queue
from common.enums import CrawlStatus
from crawler.crawl_manager import CrawlManager


class TestCrawlManager(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_start_listening_success(self):
        crawl_request = {'start_url': 'http://example.com', 'crawl_id': 'test_crawl'}
        with patch('crawler.crawl_manager.BaseCrawler') as mock_crawler, \
                patch('crawler.crawl_manager.Pool') as mock_pool:
            mock_crawler_instance = Mock()
            mock_crawler.return_value = mock_crawler_instance
            mock_crawler_instance.crawl.return_value = {'status': CrawlStatus.COMPLETE, 'crawl_id': 'test_crawl'}

            crawl_manager = CrawlManager(crawler_class=mock_crawler, queue=self.queue, max_parallel_jobs=1)

            with self.assertLogs() as log:
                crawl_manager.start_listening()

            # Assertions
            self.assertIn('Waiting for new crawl request...', log.output)
            self.assertIn(f'Received crawl request: {crawl_request}', log.output)
            mock_crawler.assert_called_once_with(start_url='http://example.com', crawl_id='test_crawl')
            mock_crawler_instance.crawl.assert_called_once()
            mock_pool.assert_called_once()
            mock_pool.return_value.apply_async.assert_called_once_with(mock_crawler_instance.crawl,
                                                                       callback=crawl_manager.handle_crawl_result)
            self.assertIn(f'Crawl request added to processing queue. crawl_id: test_crawl', log.output)
            self.assertIn(f'Crawl request {CrawlStatus.COMPLETE}. crawl_id: test_crawl', log.output)
            self.queue.put(crawl_request)  # Put a crawl request in the queue to exit the loop

    def test_start_listening_error(self):
        crawl_request = {'start_url': 'http://example.com', 'crawl_id': 'test_crawl'}
        with patch('crawler.crawl_manager.BaseCrawler') as mock_crawler, \
                patch('crawler.crawl_manager.Pool') as mock_pool:
            mock_crawler.side_effect = ValueError('Mocked error')

            crawl_manager = CrawlManager(crawler_class=mock_crawler, queue=self.queue, max_parallel_jobs=1)

            with self.assertLogs() as log:
                crawl_manager.start_listening()

            # Assertions
            self.assertIn('Waiting for new crawl request...', log.output)
            self.assertIn(f'Received crawl request: {crawl_request}', log.output)
            mock_crawler.assert_called_once_with(start_url='http://example.com', crawl_id='test_crawl')
            mock_pool.assert_not_called()
            self.assertIn(f'Error processing crawl request: Mocked error', log.output)
            self.queue.put(crawl_request)  # Put a crawl request in the queue to exit the loop


if __name__ == '__main__':
    unittest.main()
