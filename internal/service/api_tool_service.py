from dataclasses import dataclass
from injector import inject
from typing import Any
from internal.exception import ValidationException
from internal.core.tools.api_tools.entities import OpenAPISchema
import json

@inject
@dataclass
class ApiToolService:
    """自定义API工具服务类"""

    @classmethod
    async def parse_openapi_schema(cls, openapi_schema_str: str) -> Any:
        """解析OpenAPI schema字符串为Python对象, 如果出错则抛出错误"""
        try:
            data = json.loads(openapi_schema_str)
            if not isinstance(data, dict):
                raise ValueError("OpenAPI schema必须是一个字典")
        except Exception as e:
            raise ValidationException(
                f"OpenAPI schema解析错误: {e}, 传递的字符串必须是符合OpenAPI规范的JSON字符串")
        return OpenAPISchema(**data)
