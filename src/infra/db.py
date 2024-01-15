import redis


def set_status(crawl_id, status):
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set(crawl_id, status)


def get_status(crawl_id):
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r.get(crawl_id)
