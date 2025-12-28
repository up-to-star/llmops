import importlib
from typing import Any

def dynamic_import(module_name: str, symbol_name: str) -> Any:
    """动态导入模块中的特定功能"""
    module = importlib.import_module(module_name)
    return getattr(module, symbol_name)

def add_attribute(attr_name: str, attr_value: Any):
    """为对象动态添加属性"""
    def decorator(func):
        setattr(func, attr_name, attr_value)
        return func
    return decorator