from pydantic import BaseModel, Field
from injector import inject, singleton
from typing import Any
from internal.core.tools.builtin_tools.entities import CategoryEntity
import os
import yaml

@singleton
@inject
class BuiltinCategoryManager(BaseModel):
    """内置分类提供工具类"""
    category_map: dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_categories()

    def _init_categories(self):
        """初始化分类"""
        if self.category_map:
            return self.category_map

        current_path = os.path.abspath(__file__)
        categories_dir = os.path.dirname(current_path)
        categories_yaml = os.path.join(categories_dir, "categories.yaml")
        with open(categories_yaml, encoding="utf-8") as f:
            categories_yaml_data = yaml.safe_load(f)
        for category_data in categories_yaml_data:
            category_entity = CategoryEntity(**category_data)
            icon_path = os.path.join(categories_dir, "icons", category_entity.icon)
            if not os.path.exists(icon_path):
                raise ValueError(f"icon file {icon_path} not found")
            with open(icon_path, "rb") as f:
                icon_content = f.read()
            self.category_map[category_entity.category] = {
                "entity": category_entity,
                "icon": icon_content
            }

    def get_category_map(self) -> dict[str, Any]:
        """获取分类映射"""
        return self.category_map
            