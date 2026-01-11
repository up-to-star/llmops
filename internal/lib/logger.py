import logging
from functools import wraps
from typing import Callable, Any
from config.logger import get_logger


class Logger:
    """日志工具类，提供便捷的日志记录方法"""

    def __init__(self, name: str):
        self._logger = get_logger(name)

    def debug(self, message: str, *args, **kwargs):
        """记录 DEBUG 级别日志"""
        self._logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """记录 INFO 级别日志"""
        self._logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """记录 WARNING 级别日志"""
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """记录 ERROR 级别日志"""
        self._logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """记录 CRITICAL 级别日志"""
        self._logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args, **kwargs):
        """记录异常信息，包含堆栈跟踪"""
        self._logger.exception(message, *args, **kwargs)


def log_function_call(logger: Logger = None):
    """
    函数调用日志装饰器

    Args:
        logger: 日志记录器实例，如果为 None 则使用默认日志记录器

    Usage:
        @log_function_call()
        def my_function():
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            func_logger = logger or Logger(func.__module__)
            func_logger.info(
                f"调用函数: {func.__name__}, 参数: args={args}, kwargs={kwargs}")
            try:
                result = await func(*args, **kwargs)
                func_logger.info(f"函数 {func.__name__} 执行成功")
                return result
            except Exception as e:
                func_logger.exception(f"函数 {func.__name__} 执行失败: {str(e)}")
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            func_logger = logger or Logger(func.__module__)
            func_logger.info(
                f"调用函数: {func.__name__}, 参数: args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                func_logger.info(f"函数 {func.__name__} 执行成功")
                return result
            except Exception as e:
                func_logger.exception(f"函数 {func.__name__} 执行失败: {str(e)}")
                raise

        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def get_module_logger(module_name: str = None) -> Logger:
    """
    获取模块日志记录器

    Args:
        module_name: 模块名称，如果为 None 则使用调用者的模块名称

    Returns:
        Logger: 日志记录器实例

    Usage:
        logger = get_module_logger(__name__)
        logger.info("这是一条日志")
    """
    if module_name is None:
        import inspect
        frame = inspect.currentframe().f_back
        module_name = frame.f_globals.get('__name__', '__main__')
    return Logger(module_name)
