import os
import logging
import logging.handlers
from pathlib import Path
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """带颜色的日志格式化器"""

    COLORS = {
        'DEBUG': '\033[36m',      # 青色
        'INFO': '\033[32m',       # 绿色
        'WARNING': '\033[33m',    # 黄色
        'ERROR': '\033[31m',       # 红色
        'CRITICAL': '\033[35m',    # 紫色
    }
    RESET = '\033[0m'

    def __init__(self, fmt=None, datefmt=None, style='%'):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        return super().format(record)


def setup_logging(
    log_level: str = "INFO",
    log_dir: Optional[str] = None,
    log_file: Optional[str] = None,
    backup_count: int = 30,
    when: str = "midnight",
    interval: int = 1,
) -> None:
    """
    配置日志系统，支持按天轮转日志文件

    Args:
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: 日志文件目录，默认为项目根目录下的 logs 文件夹
        log_file: 日志文件名，默认为 debug.log
        backup_count: 保留的日志文件备份数量，默认为 30 天
        when: 轮转时间间隔，可选值:
            - 'S' - 秒
            - 'M' - 分
            - 'H' - 小时
            - 'D' - 天
            - 'midnight' - 每天午夜（默认）
            - 'W0'-'W6' - 每周某天（0=周一，6=周日）
        interval: 时间间隔的数量，默认为 1
    """
    log_level = os.getenv("LOG_LEVEL", log_level).upper()

    if log_dir is None:
        log_dir = Path(__file__).parent.parent / "logs"
    else:
        log_dir = Path(log_dir)

    if log_file is None:
        log_file = "debug.log"

    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / log_file

    numeric_level = getattr(logging, log_level, logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    root_logger.handlers.clear()

    colored_formatter = ColoredFormatter(
        fmt="[%(asctime)s - %(levelname)s]:   %(name)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    plain_formatter = logging.Formatter(
        fmt="[%(asctime)s - %(levelname)s]:   %(name)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(colored_formatter)
    root_logger.addHandler(console_handler)

    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=str(log_path),
        when=when,
        interval=interval,
        backupCount=backup_count,
        encoding="utf-8",
        atTime=None
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(plain_formatter)
    file_handler.suffix = "%Y-%m-%d.log"
    root_logger.addHandler(file_handler)

    error_log_path = log_dir / "error.log"
    error_handler = logging.handlers.TimedRotatingFileHandler(
        filename=str(error_log_path),
        when=when,
        interval=interval,
        backupCount=backup_count,
        encoding="utf-8",
        atTime=None
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(plain_formatter)
    error_handler.suffix = "%Y-%m-%d.log"
    root_logger.addHandler(error_handler)


def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的日志记录器

    Args:
        name: 日志记录器名称，通常使用 __name__

    Returns:
        logging.Logger: 日志记录器实例
    """
    return logging.getLogger(name)
