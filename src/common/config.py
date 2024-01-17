from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 6379
    DB_DB: int = 0


class WebAppConfig(BaseSettings):
    WEBAPP_HOST: str = '0.0.0.0'
    WEBAPP_PORT: int = 8000


class CommonConfig(BaseSettings):
    crawler_max_parallel_jobs: int = 1
    workdir: str = 'crawl_jobs'
