from injector import Injector
from pydantic import BaseModel, create_model, Field
from dataclasses import dataclass
from langchain.tools import BaseTool
from langchain_core.tools import StructuredTool
from typing import Type, Optional, Callable
from internal.core.tools.api_tools.entities import ParamaterType, ParameterTypeMap, ToolEntity, ParameterIn
import requests


@Injector
@dataclass
class ApiProviderManager(BaseModel):

    @classmethod
    def _create_model_from_parameters(cls, params: list[dict]) -> Type[BaseModel]:
        """根据参数列表创建模型"""
        fields = {}
        for param in params:
            field_name = param.get("name")
            field_type = ParameterTypeMap.get(
                param.get("type", ParamaterType.STR), str)
            field_required = param.get("required", True)
            field_description = param.get("description", "")
            fields[field_name] = (
                field_type if field_required else Optional[field_type],
                Field(description=field_description)
            )
        return create_model(
            "DynamicModel",
            **fields
        )

    def get_tool(self, tool_entity: ToolEntity) -> BaseTool:
        """根据工具实体获取对应的工具"""
        return StructuredTool.from_function(
            func=self._create_tool_func_from_tool_entity(tool_entity),
            name=f"{tool_entity.id}-{tool_entity.name}",
            description=tool_entity.description,
            args_schema=self._create_model_from_parameters(
                tool_entity.parameters),
        )

    @classmethod
    def _create_tool_func_from_tool_entity(cls, tool_entity: ToolEntity) -> Callable:
        """根据工具实体创建对应的函数"""
        def tool_func(**kwargs) -> str:
            """API工具请求函数"""
            parameters = {
                ParameterIn.PATH: {},
                ParameterIn.QUERY: {},
                ParameterIn.HEADER: {},
                ParameterIn.COOKIE: {},
                ParameterIn.REQUEST_BODY: {},
            }

            parameters_map = {parameter.get(
                "name"): parameter for parameter in tool_entity.parameters}
            header_map = {header.get("key"): header.get("value")
                          for header in tool_entity.headers}
            for key, value in kwargs.items():
                parameter = parameters_map.get(key)
                if not parameter:
                    continue
                parameters[parameter.get("in", ParameterIn.QUERY)][key] = value

            return requests.request(
                method=tool_entity.method,
                url=tool_entity.url.format(**parameters[ParameterIn.PATH]),
                headers={**header_map, **parameters[ParameterIn.HEADER]},
                params=parameters[ParameterIn.QUERY],
                json=parameters[ParameterIn.REQUEST_BODY],
                cookies=parameters[ParameterIn.COOKIE],
            ).text

        return tool_func
