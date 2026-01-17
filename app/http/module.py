
import redis.asyncio as async_redis
import dotenv
from config.config import REDIS_CONFIG
from injector import Module, provider, singleton, Injector
from config.di_config import RedisModule, ServiceModule

dotenv.load_dotenv()


