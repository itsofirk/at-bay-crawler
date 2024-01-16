import logging
from multiprocessing import Pool
from typing import Type

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

    def start_listening(self):
        with Pool(processes=self.max_parallel_jobs) as pool:
            while True:
                logger.info('Waiting for new crawl request...')
                crawl_request = self.queue.get()
                logger.info(f'Received crawl request: {crawl_request}')
                try:
                    self._validate_crawl_request(crawl_request)
                    crawler = self.crawler_class(**crawl_request, **self.crawler_kwargs)
                    # Process the crawl request asynchronously
                    pool.apply(crawler.crawl)
                    logger.info(f'Crawl request added to processing queue. crawl_id: {crawl_request["crawl_id"]}')
                except Exception as e:
                    logger.error(f'Error processing crawl request: {str(e)}')
