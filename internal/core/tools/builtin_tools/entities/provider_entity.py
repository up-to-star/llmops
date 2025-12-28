from pydantic import BaseModel, Field
import yaml
import os
from .tool_entity import ToolEntity
from internal.lib import dynamic_import
from typing import Any
import time


class ProviderEntity(BaseModel):
    """服务商实体类, 映射的数据是providers.yaml文件中的数据"""
    name: str = Field(description="服务商名称")
    label: str = Field(description="服务商显示名称")
    description: str = Field(description="服务商描述")
    icon: str = Field(description="服务商图标")
    background: str = Field(description="服务商图标背景颜色")
    category: str = Field(description="服务商分类")
    create_at: int = Field(default_factory=lambda: int(time.time()), description="服务商创建时间")


class Provider(BaseModel):
    """服务提供商，在该类下可以获取该服务提供商的所有工具、描述、图标等多个信息"""
    name: str = Field(description="服务商名称")
    position: int = Field(description="服务商排序位置")
    provider_entity: ProviderEntity = Field(description="服务商实体类")
    tool_entity_map: dict[str, ToolEntity] = Field(
        default_factory=dict, description="服务商工具实体类映射")
    tool_func_map: dict[str, Any] = Field(
        default_factory=dict, description="服务商工具函数映射")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._provider_init()

    class Config:
        """Pydantic配置类"""
        protected_namespaces = ()

    def get_tool(self, tool_name: str) -> Any:
        """根据工具名称获取服务商的工具函数"""
        return self.tool_func_map.get(tool_name)

    def get_tool_entity(self, tool_name: str) -> ToolEntity:
        """根据工具名称获取服务商的工具实体类"""
        tool_entity = self.tool_entity_map.get(tool_name)
        if not tool_entity:
            raise ValueError(f"工具 {tool_name} 不存在")
        return tool_entity

    def get_tool_entities(self) -> list[ToolEntity]:
        """获取服务商的所有工具实体类"""
        return list(self.tool_entity_map.values())

    def _provider_init(self):
        """服务商初始化"""
        current_path = os.path.abspath(__file__)
        entities_path = os.path.dirname(current_path)
        provider_path = os.path.join(os.path.dirname(
            entities_path), "providers", self.name)
        position_yaml_path = os.path.join(provider_path, "positions.yaml")
        with open(position_yaml_path, encoding="utf-8") as f:
            position_yaml_data = yaml.safe_load(f)
        for tool_name in position_yaml_data:
            tool_yaml_path = os.path.join(provider_path, f"{tool_name}.yaml")
            with open(tool_yaml_path, encoding="utf-8") as f:
                tool_yaml_data = yaml.safe_load(f)
                self.tool_entity_map[tool_name] = ToolEntity(**tool_yaml_data)

            self.tool_func_map[tool_name] = dynamic_import(
                f"internal.core.tools.builtin_tools.providers.{self.name}",
                tool_name
            )
