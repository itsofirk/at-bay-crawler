import logging
from multiprocessing import Pool

from scrapy.crawler import CrawlerProcess
from crawler.scrapy_spider import ScrapySpider
from infra.base_storage import BaseStorage
from infra.db import set_status
from common.enums import CrawlStatus

logger = logging.getLogger(__name__)


class CrawlManager:
    def __init__(self, feed_storage: BaseStorage, queue, max_parallel_jobs: int = 1):
        self.max_parallel_jobs = max_parallel_jobs
        self.feed_storage = feed_storage
        self.queue = queue
        logger.info('Crawl manager initialized successfully.')

    def start_listening(self):
        with Pool(processes=self.max_parallel_jobs) as pool:
            while True:
                logger.info('Waiting for new crawl request...')
                crawl_request = self.queue.get()
                logger.info(f'Received crawl request: {crawl_request}')
                try:
                    job = CrawlJob(self.feed_storage, crawl_request)
                    # Process the crawl request asynchronously
                    pool.apply(job.process_crawl_request)
                    logger.info(f'Crawl request added to processing queue. crawl_id: {crawl_request["crawl_id"]}')
                except Exception as e:
                    logger.error(f'Error processing crawl request: {str(e)}')


class CrawlJob:
    def __init__(self, feed_storage: BaseStorage, crawl_request: dict):
        self.feed_storage = feed_storage
        self.crawl_request = crawl_request

    def process_crawl_request(self):
        crawl_id = self.crawl_request['crawl_id']
        logger.info(f'Processing crawl request: {crawl_id}')
        set_status(crawl_id, CrawlStatus.RUNNING.value)
        self.start_scrapy_crawler(crawl_id)
        set_status(crawl_id, CrawlStatus.COMPLETE.value)

    def start_scrapy_crawler(self, job_id):
        try:
            process = CrawlerProcess(settings={
                'FEEDS': {
                    'items.json': {'format': 'json'},
                },
            })
            process.crawl(ScrapySpider, feed_storage=self.feed_storage, crawl_request=self.crawl_request)
            process.start()
            logger.info(f'Scrapy crawler started successfully for crawl_id: {job_id}')
        except Exception as e:
            logger.error(f'Error starting Scrapy crawler: {str(e)}')
