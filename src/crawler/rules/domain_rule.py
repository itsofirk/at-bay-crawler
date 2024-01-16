from crawler.rules import BaseRule


class DomainRule(BaseRule):
    def __init__(self, allowed_domain):
        self.allowed_domain = allowed_domain

    def check(self, url):
        return self.allowed_domain in url
