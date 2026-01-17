from internal.server import Http
from internal.router import Router
from config.logger import setup_logging
import os
import dotenv
from config.di_config import injector

dotenv.load_dotenv()

setup_logging(
    log_level=os.getenv("LOG_LEVEL", "INFO"),
    log_dir=os.getenv("LOG_DIR", "./logs"),
    log_file=os.getenv("LOG_FILE", "app.log"),
    backup_count=30,
)


# 创建应用实例
app = Http(router=injector.get(Router))
