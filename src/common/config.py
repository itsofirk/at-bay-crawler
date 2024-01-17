from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 6379
    DB_DB: int = 0


class WebAppConfig(BaseSettings):
    CRAWLER_MAX_PARALLEL_JOBS: int = 1
    WEBAPP_HOST: str = '0.0.0.0'
    WEBAPP_PORT: int = 8000
    BASE_DIR: str = 'crawl_jobs'
