import logging
from multiprocessing import Pool
from typing import Type

from common.enums import CrawlStatus
from infra.db import set_status
from crawler.base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class CrawlManager:
    def __init__(self, crawler_class: Type[BaseCrawler], queue, max_parallel_jobs: int = 1, **crawler_kwargs):
        self.max_parallel_jobs = max_parallel_jobs
        self.queue = queue
        self.crawler_class = crawler_class
        self.crawler_kwargs = crawler_kwargs
        self._validate_crawler_kwargs()
        logger.info('Crawl manager initialized successfully.')

    def _validate_crawler_kwargs(self):
        if 'start_url' in self.crawler_kwargs:
            raise ValueError('start_url cannot be provided as a kwarg')
        if 'crawl_id' in self.crawler_kwargs:
            raise ValueError('crawl_id cannot be provided as a kwarg')

    def _validate_crawl_request(self, crawl_request: dict):
        if 'start_url' not in crawl_request:
            raise ValueError('start_url must be provided in the crawl request')
        if 'crawl_id' not in crawl_request:
            raise ValueError('crawl_id must be provided in the crawl request')

    def update_status(self, crawl_id: str, status: CrawlStatus, **kwargs):
        set_status(crawl_id, status, **kwargs)

    def start_listening(self):
        with Pool(processes=self.max_parallel_jobs) as pool:
            while True:
                logger.info('Waiting for new crawl request...')
                crawl_request = self.queue.get()
                logger.info(f'Received crawl request: {crawl_request}')
                try:
                    self._validate_crawl_request(crawl_request)
                    crawler = self.crawler_class(**crawl_request, **self.crawler_kwargs)
                    self.update_status(crawl_request["crawl_id"], CrawlStatus.RUNNING)
                    # Process the crawl request asynchronously
                    pool.apply_async(crawler.crawl, callback=self.success_callback, error_callback=self.fail_callback)
                    logger.info(f'Crawl request added to processing queue. crawl_id: {crawl_request["crawl_id"]}')
                except Exception as e:
                    logger.error(f'Error processing crawl request: {str(e)}')

    def handle_crawl_result(self, result, status):
        logger.info(f'Crawl request {status}. crawl_id: {result["crawl_id"]}')
        crawl_id = result.pop("crawl_id")
        assert result.pop("status") == status

        self.update_status(crawl_id, status, **result)

    def success_callback(self, result):
        self.handle_crawl_result(result, CrawlStatus.COMPLETE)

    def fail_callback(self, result):
        self.handle_crawl_result(result, CrawlStatus.ERROR)
