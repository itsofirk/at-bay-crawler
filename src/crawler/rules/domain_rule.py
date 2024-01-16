from urllib.parse import urlparse

from crawler.rules import BaseRule


class DomainRule(BaseRule):
    def __init__(self, start_url):
        start_url_domain = urlparse(start_url).netloc
        assert start_url_domain is not None, "Invalid start URL"
        self.allowed_domain = start_url_domain

    def check(self, url):
        return self.allowed_domain in url
