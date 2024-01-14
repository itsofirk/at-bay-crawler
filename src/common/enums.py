from enum import Enum


class CrawlStatus(Enum):
    ACCEPTED = "Accepted"
    RUNNING = "Running"
    ERROR = "Error"
    COMPLETE = "Complete"
    NOT_FOUND = "Not-Found"
