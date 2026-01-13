import os
import redis.asyncio as redis
from tortoise import Tortoise
import dotenv
from fastapi import FastAPI
from .logger import get_logger
from celery import Celery

logger = get_logger(__name__)


dotenv.load_dotenv()

# 从环境变量获取数据库配置
DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": os.getenv("MYSQL_HOST", "localhost"),
                "port": int(os.getenv("MYSQL_PORT", 13316)),
                "user": os.getenv("MYSQL_USER", "root"),
                "password": os.getenv("MYSQL_ROOT_PASSWORD", "123"),
                "database": os.getenv("MYSQL_DATABASE", "llmops_db"),
            },
        },
    },
    "apps": {
        "models": {
            "models": ["internal.model"],  # 数据库模型所在的模块
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}

REDIS_CONFIG = {
    "url": f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}",
    "db": int(os.getenv("REDIS_DB", 0)),
    "password": os.getenv("REDIS_PASSWORD", None),
    "encoding": "utf-8",
    "decode_responses": True,
    "max_connections": 50,
    # "socket_connection_timeout": 5,
    "socket_timeout": 5,
    "retry_on_timeout": True,
    "health_check_interval": 30,
    # "ssl": os.getenv("REDIS_USE_SSL", False),
}


async def init_db():
    """初始化数据库连接"""
    await Tortoise.init(config=DB_CONFIG)
    # 如果设置为True，会自动创建数据库表（生产环境建议关闭）
    await Tortoise.generate_schemas()


async def close_db():
    """关闭数据库连接"""
    await Tortoise.close_connections()


async def init_redis(app: FastAPI):
    """初始化redis连接"""
    app.state.redis_pool = redis.ConnectionPool.from_url(**REDIS_CONFIG)
    app.state.redis = redis.Redis(connection_pool=app.state.redis_pool)


async def close_redis(app: FastAPI):
    """关闭redis连接"""
    if hasattr(app.state, "redis"):
        await app.state.redis.close()
    if hasattr(app.state, "redis_pool"):
        app.state.redis_pool.disconnect()

celery_app = Celery(
    "llmops",
    broker=os.getenv(
        f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 16379)}/{os.getenv('CELERY_BROKER_DB', 1)}",
        "redis://localhost:16379/1"),
    backend=os.getenv(f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 16379)}/{os.getenv('CELERY_RESULT_BACKEND_DB', 1)}",
                      "redis://localhost:16379/1"),
    include=["internal.tasks.demo_task"]
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
    task_ignore_result=bool(os.getenv("CELERY_TASK_IGNORE_RESULT", False)),
    result_expires=int(os.getenv("CELERY_RESULT_EXPIRES", 3600)),
)
