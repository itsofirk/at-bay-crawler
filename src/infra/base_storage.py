from abc import ABC


class BaseStorage(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def save_html(self, crawl_id, url, html) -> str:
        pass

    def save_crawl_request(self, crawl_id, start_url):
        pass
