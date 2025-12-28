from injector import inject
from dataclasses import dataclass
from internal.service.builtin_tool_service import BuiltinToolService
from pkg.response import HttpCode, Response

@inject
@dataclass
class BuiltinToolHandler:
    """内置工具处理器"""
    builtin_tool_service: BuiltinToolService

    async def get_builtin_tools(self):
        """获取所有内置工具信息和提供商信息"""
        builtin_tools =  await self.builtin_tool_service.get_builtin_tools()
        response = Response(
            code=HttpCode.SUCCESS,
            message="获取所有内置工具信息和提供商信息成功",
            data=builtin_tools,
        )
        return response

    async def get_provider_tool(self, provider_name: str, tool_name: str):
        """获取指定提供商的指定工具信息"""
        tool = await self.builtin_tool_service.get_provider_tool(
            provider_name, tool_name)
        response = Response(
            code=HttpCode.SUCCESS,
            message="获取指定提供商的指定工具信息成功",
            data=tool,
        )
        return response
