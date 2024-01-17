from pydantic_settings import BaseSettings


class RedisConfig(BaseSettings):
    class Config:
        env_prefix = 'REDIS_'

    host: str = 'localhost'
    port: int = 6379
    db_index: int = 0


class WebAppConfig(BaseSettings):
    class Config:
        env_prefix = 'WEBAPP_'
    host: str = '0.0.0.0'
    port: int = 8000


class CommonConfig(BaseSettings):
    crawler_max_parallel_jobs: int = 1
    workdir: str = 'crawl_jobs'
