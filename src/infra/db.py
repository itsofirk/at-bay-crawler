import logging
import redis

logger = logging.getLogger(__name__)


def set_status(crawl_id, status):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.set(crawl_id, status)
        logger.info(f'Status set successfully. crawl_id: {crawl_id}, status: {status}')
    except Exception as e:
        logger.error(f'Error setting status: {str(e)}')


def get_status(crawl_id):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        status = r.get(crawl_id)
        logger.info(f'Status retrieved successfully. crawl_id: {crawl_id}, status: {status}')
        return status
    except Exception as e:
        logger.error(f'Error getting status: {str(e)}')
        return None
