import os
from tortoise import Tortoise
import dotenv

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


async def init_db():
    """初始化数据库连接"""
    await Tortoise.init(config=DB_CONFIG)
    # 如果设置为True，会自动创建数据库表（生产环境建议关闭）
    await Tortoise.generate_schemas()


async def close_db():
    """关闭数据库连接"""
    await Tortoise.close_connections()
