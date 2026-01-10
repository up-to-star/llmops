import mimetypes
from injector import inject
from dataclasses import dataclass
from internal.core.tools.builtin_tools.providers import BuiltinProviderManager
from internal.core.tools.builtin_tools.categories import BuiltinCategoryManager
from pydantic import BaseModel
from typing import Any
from internal.exception import NotFoundException
import os


@inject
@dataclass
class BuiltinToolService:
    """内置工具服务类"""
    builtin_provider_manager: BuiltinProviderManager
    builtin_category_manager: BuiltinCategoryManager

    async def get_provider_icon(self, provider_name: str) -> tuple[bytes, str]:
        """根据服务商名称获取服务商图标"""
        provider = self.builtin_provider_manager.get_provider(provider_name)
        if not provider:
            raise NotFoundException(f"Provider {provider_name} not found")
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        provider_path = os.path.join(
            root_path, "core", "tools", "builtin_tools", "providers", provider_name)
        icon_path = os.path.join(
            provider_path, "_asset", provider.provider_entity.icon)
        if not os.path.exists(icon_path):
            raise NotFoundException(
                f"Icon for provider {provider_name} not found")
        mimetype, _ = mimetypes.guess_type(icon_path)
        mimetype = mimetype or "application/octet-stream"
        return icon_path, mimetype

    async def get_categories(self) -> list:
        """获取所有工具分类"""
        category_map = self.builtin_category_manager.get_category_map()
        
        return [{
            "name": category["entity"].name,
            "category": category["entity"].category,
            "icon": category["icon"]
        } for category in category_map.values()]
        
    async def get_builtin_tools(self) -> list:
        """获取所有内置工具"""
        providers = self.builtin_provider_manager.get_providers()
        builtin_tools = []
        for provider in providers:
            provider_entity = provider.provider_entity
            builtin_tool = {
                **provider_entity.model_dump(exclude=["icon"]),
                "tools": []
            }
            for tool_entity in provider.get_tool_entities():
                tool = provider.get_tool(tool_entity.name)
                tool_dict = {
                    **tool_entity.model_dump(),
                    "inputs": self.get_tool_inputs(tool)
                }
                builtin_tool["tools"].append(tool_dict)
            builtin_tools.append(builtin_tool)
        return builtin_tools

    async def get_provider_tool(self, provider_name: str, tool_name: str) -> Any:
        """根据服务商名称和工具名称获取内置工具"""
        provider = self.builtin_provider_manager.get_provider(provider_name)
        if not provider:
            raise NotFoundException(f"Provider {provider_name} not found")
        tool_entity = provider.get_tool_entity(tool_name)
        if not tool_entity:
            raise NotFoundException(
                f"Tool {tool_name} not found in provider {provider_name}")
        provider_entity = provider.provider_entity
        tool = provider.get_tool(tool_entity.name)
        builtin_tool = {
            "provider": {**provider_entity.model_dump(exclude=["icon", "create_at"])},
            **tool_entity.model_dump(),
            "inputs": self.get_tool_inputs(tool),
            "create_at": provider_entity.create_at
        }
        return builtin_tool

    @classmethod
    def get_tool_inputs(cls, tool) -> list:
        inputs = []
        if hasattr(tool, "args_schema") and issubclass(tool.args_schema, BaseModel):
            for field_name, model_field in tool.args_schema.model_fields.items():
                inputs.append({
                    "name": field_name,
                    "description": model_field.description or "",
                    "required": model_field.is_required(),
                    "type": model_field.annotation.__name__
                })
        return inputs
