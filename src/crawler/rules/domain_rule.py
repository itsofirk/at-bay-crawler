from urllib.parse import urlparse, ParseResult

from crawler.rules import BaseRule


class DomainRule(BaseRule):
    def __init__(self, start_url):
        start_url_domain = urlparse(start_url).netloc
        assert start_url_domain is not None, "Invalid start URL"
        self.allowed_domain = start_url_domain.lstrip("www.")

    def check(self, url):
        if not isinstance(url, ParseResult):
            url = urlparse(url)
        return self.allowed_domain in url.netloc
