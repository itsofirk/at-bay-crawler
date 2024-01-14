from webapp.models import CrawlRequest


class Spider:
    @staticmethod
    def initiate_crawl(crawl_request: CrawlRequest):
        ...

    @staticmethod
    def get_crawl_status(crawl_id: str):
        ...
