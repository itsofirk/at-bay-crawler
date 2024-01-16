from common.enums import CrawlStatus
from crawler.crawl_manager import logger
from crawler.scrapy_spider import ScrapySpider
from infra.base_storage import BaseStorage
from infra.db import set_status


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
