from dataclasses import dataclass
from injector import inject
from typing import Any
from internal.exception import ValidationException, NotFoundException
from internal.core.tools.api_tools.entities import OpenAPISchema
from internal.model import ApiToolProvider, ApiTool
from internal.schema import CreateApiToolRequest, GetApiToolProvidersWithPageRequest
import json
import uuid
from pkg.paginator import BaseQuery, Paginator


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

    async def create_api_tool(self, req: CreateApiToolRequest):
        """创建自定义API工具"""
        account_id = "550e8400-e29b-41d4-a716-446655440000"
        openapi_schema = await self.parse_openapi_schema(req.openapi_schema)
        api_tool_provider = await ApiToolProvider.filter(account_id=account_id, name=req.name).first()
        if api_tool_provider:
            raise ValidationException(f"API工具供应商 {req.name} 已存在")
        serializable_headers = [item.model_dump() for item in req.headers]
        api_tool_provider = ApiToolProvider(
            account_id=account_id,
            name=req.name,
            icon=req.icon,
            description=openapi_schema.description,
            openapi_schema=req.openapi_schema,
            headers=serializable_headers
        )
        await api_tool_provider.save()

        for path, path_item in openapi_schema.paths.items():
            for method, operation in path_item.items():
                api_tool = ApiTool(
                    account_id=account_id,
                    provider_id=api_tool_provider.id,
                    name=operation.get("operationId"),
                    description=operation.get("description"),
                    url=f"{openapi_schema.server}{path}",
                    method=method.upper(),
                    parameters=operation.get("parameters", []),
                )
                await api_tool.save()

    async def get_api_tool_provider(self, provider_id: uuid.UUID) -> ApiToolProvider:
        """获取自定义API工具供应商"""
        account_id = "550e8400-e29b-41d4-a716-446655440000"
        api_tool_provider = await ApiToolProvider.filter(id=provider_id).first()
        if not api_tool_provider or str(api_tool_provider.account_id) != account_id:
            raise NotFoundException(f"API工具供应商 {provider_id} 不存在")
        return api_tool_provider

    async def get_api_tool(self, provider_id: uuid.UUID, tool_name: str) -> ApiTool:
        """获取自定义API工具详细信息"""
        account_id = "550e8400-e29b-41d4-a716-446655440000"
        api_tool = await ApiTool.filter(
            provider=provider_id,
            name=tool_name
        ).prefetch_related("provider").first()  # 预加载关联数据
        if not api_tool or str(api_tool.account_id) != account_id:
            raise NotFoundException(f"API工具 {tool_name} 不存在")
        return api_tool

    async def delete_api_tool_provider(self, provider_id: uuid.UUID):
        """根据provider_id删除自定义API工具供应商信息"""
        account_id = "550e8400-e29b-41d4-a716-446655440000"
        api_tool_provider = await ApiToolProvider.filter(id=provider_id).first()
        if not api_tool_provider or str(api_tool_provider.account_id) != account_id:
            raise NotFoundException(f"API工具供应商 {provider_id} 不存在")

        await ApiTool.filter(provider=provider_id, account_id=account_id).all().delete()

        await api_tool_provider.delete()

    async def get_api_tool_providers_with_page(self, req: GetApiToolProvidersWithPageRequest) -> tuple[list[Any], Paginator]:
        """获取API工具供应商列表信息，支持分页"""
        account_id = "550e8400-e29b-41d4-a716-446655440000"
        filter = ApiToolProvider.filter(account_id=account_id)
        if req.search_word:
            filter = filter.filter(name__contains=req.search_word)
        filter = filter.prefetch_related("tools")
        query = BaseQuery(ApiToolProvider, req.current_page, req.page_size)
        api_tool_providers, paginator = await query.paginate(filter)

        
        return api_tool_providers, paginator
