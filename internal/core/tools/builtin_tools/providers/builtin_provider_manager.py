from typing import Any
from injector import inject, singleton
import os
import yaml
from internal.core.tools.builtin_tools.entities import ProviderEntity, Provider, ToolEntity


@singleton
@inject
class BuiltinProviderManager:
    """内置服务商提供工具类"""
    provider_map: dict[str, Provider] = {}

    def __init__(self):
        self._get_provider_map()

    def get_provider(self, provider_name: str) -> Provider:
        """获取服务商"""
        return self.provider_map.get(provider_name)

    def get_providers(self) -> list[Provider]:
        """获取所有服务商"""
        return list(self.provider_map.values())

    def get_provider_entities(self) -> list[ProviderEntity]:
        """获取所有服务商实体"""
        return [provider.provider_entity for provider in self.get_providers()]

    def get_tool(self, provider_name: str, tool_name: str) -> Any:
        """根据服务商名称和工具名称获取服务商工具"""
        provider = self.get_provider(provider_name)
        if not provider:
            return None
        return provider.get_tool(tool_name)

    def _get_provider_map(self):
        """获取服务商映射"""
        if self.provider_map:
            return self.provider_map

        current_path = os.path.abspath(__file__)
        providers_dir = os.path.dirname(current_path)
        providers_yaml = os.path.join(providers_dir, "providers.yaml")
        with open(providers_yaml, encoding="utf-8") as f:
            providers_yaml_data = yaml.safe_load(f)
        for idx, provider_data in enumerate(providers_yaml_data):
            provider_entity = ProviderEntity(**provider_data)
            self.provider_map[provider_entity.name] = Provider(
                name=provider_entity.name,
                position=idx + 1,
                provider_entity=provider_entity
            )
