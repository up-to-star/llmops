import importlib
from typing import Any

def dynamic_import(module_name: str, symbol_name: str) -> Any:
    """动态导入模块中的特定功能"""
    module = importlib.import_module(module_name)
    return getattr(module, symbol_name)
