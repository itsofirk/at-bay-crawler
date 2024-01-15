import logging

from scrapy.crawler import CrawlerProcess
from crawler.scrapy_spider import ScrapySpider
from infra.base_storage import BaseStorage
from infra.db import set_status
from infra.queue import queue
from common.enums import CrawlStatus
from multiprocessing import Pool

logger = logging.getLogger(__name__)


class CrawlManager:
    def __init__(self, feed_storage: BaseStorage, max_parallel_jobs: int = 1):
        self.max_parallel_jobs = max_parallel_jobs
        self.feed_storage = feed_storage

    def start_listening(self):
        while True:
            crawl_request = queue.get()  # Get the crawl request from the queue
            try:
                # Create a pool of worker processes
                with Pool(processes=self.max_parallel_jobs) as pool:
                    # Process the crawl request asynchronously
                    pool.apply_async(self.process_crawl_request, (crawl_request,))
                logger.info(f'Crawl request added to processing queue. crawl_id: {crawl_request["crawl_id"]}')
            except Exception as e:
                logger.error(f'Error processing crawl request: {str(e)}')

    def process_crawl_request(self, crawl_request):
        crawl_id = crawl_request['crawl_id']
        set_status(crawl_id, CrawlStatus.RUNNING.value)
        self._start_scrapy_crawler(crawl_id, crawl_request)
        set_status(crawl_id, CrawlStatus.COMPLETE.value)

    def _start_scrapy_crawler(self, job_id, crawl_requests):
        try:
            process = CrawlerProcess(settings={
                'FEEDS': {
                    'items.json': {'format': 'json'},
                },
            })
            for crawl_request in crawl_requests:
                process.crawl(ScrapySpider, feed_storage=self.feed_storage, crawl_request=crawl_request)
            process.start()
            logger.info(f'Scrapy crawler started successfully for crawl_id: {job_id}')
        except Exception as e:
            logger.error(f'Error starting Scrapy crawler: {str(e)}')
