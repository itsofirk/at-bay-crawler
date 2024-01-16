class BaseRule:
    def check(self, url):
        raise NotImplementedError("Subclasses must implement the check method")
