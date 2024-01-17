from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    db_host: str = 'localhost'
    db_port: int = 6379
    db_db: int = 0


class WebAppConfig(BaseSettings):
    host: str = '0.0.0.0'
    port: int = 8000


class CommonConfig(BaseSettings):
    crawler_max_parallel_jobs: int = 1
    workdir: str = 'crawl_jobs'
