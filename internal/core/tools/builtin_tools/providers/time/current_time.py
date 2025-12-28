from langchain.tools import BaseTool
from datetime import datetime
from typing import Any

class CurrentTimeTool(BaseTool):
    """获取当前时间工具"""
    name: str = "current_time"
    description: str = "用于获取当前时间的工具"

    def _run(self, *args: Any, **kwargs: Any) -> str:
        """获取当前系统的时间并进行格式化返回"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")

def current_time() -> BaseTool:
    """返回获取当前时间的工具"""
    return CurrentTimeTool()
