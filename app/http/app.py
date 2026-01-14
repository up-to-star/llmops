from injector import Injector, Module, provider, singleton
from internal.server import Http
from internal.router import Router
from config.logger import setup_logging
from config.config import REDIS_CONFIG
import redis
import redis.asyncio as async_redis
import os
import dotenv

dotenv.load_dotenv()

setup_logging(
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_dir=os.getenv("LOG_DIR", "./logs"),
    log_file=os.getenv("LOG_FILE", "app.log"),
    backup_count=30,
)


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

# 创建应用实例
app = Http(router=injector.get(Router))
