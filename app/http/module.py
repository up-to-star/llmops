import redis
import redis.asyncio as async_redis
import os
import dotenv
from config.config import REDIS_CONFIG
from injector import Module, provider, singleton, Injector

dotenv.load_dotenv()


class RedisModule(Module):
    @singleton
    @provider
    def provide_async_redis(self) -> async_redis.Redis:
        return async_redis.Redis(connection_pool=async_redis.ConnectionPool.from_url(**REDIS_CONFIG))

    @singleton
    @provider
    def provide_sync_redis(self) -> redis.Redis:
        return redis.Redis.from_url(**REDIS_CONFIG)


# 创建依赖注入容器
injector = Injector([RedisModule()])