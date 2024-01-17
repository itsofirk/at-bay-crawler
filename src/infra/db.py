import atexit
import logging
import redis

from common.enums import CrawlStatus
from common.config import RedisConfig

logger = logging.getLogger(__name__)
_config = RedisConfig()

conn = redis.Redis(host=_config.host, port=_config.port, db=_config.db_index)
atexit.register(conn.close)


def set_status(crawl_id: str, status: CrawlStatus, **data):
    try:
        # data.update({'status': status})
        conn.hset(crawl_id, 'status', status.value, mapping=data)
        logger.debug(f'Status set successfully. crawl_id: {crawl_id}, status: {status}')
    except Exception as e:
        logger.error(f'Error setting status: {str(e)}')


def get_status(crawl_id):
    try:
        status = conn.hget(crawl_id, 'status')
        logger.info(f'Status retrieved successfully. crawl_id: {crawl_id}, status: {status}')
        return CrawlStatus(status)
    except Exception as e:
        logger.error(f'Error getting status: {str(e)}')
        return CrawlStatus.NOT_FOUND


def get_crawl(crawl_id):
    try:
        data = conn.hgetall(crawl_id)
        data = {key.decode('utf-8'): value.decode('utf-8') for key, value in data.items()}
        return data
    except Exception as e:
        logger.error(f'Error getting data: {str(e)}')
        return {'status': CrawlStatus.NOT_FOUND.value}
