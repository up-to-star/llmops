from injector import inject
from dataclasses import dataclass
from internal.schema import (ValidateOpenApiSchemaRequest, CreateApiToolRequest,
                             GetApiToolProviderResponse, GetApiToolResponse, GetApiToolProvidersWithPageRequest, GetApiToolProvidersWithPageResponse, UpdateApiToolProviderRequest)
from internal.service import ApiToolService
from pkg.response import HttpCode, Response
from pkg.paginator import PageModel
import uuid


@inject
@dataclass
class ApiToolHandler:
    """自定义API工具处理类"""
    api_tool_service: ApiToolService

    async def get_api_tool(self, provider_id: uuid.UUID, tool_name: str):
        """获取自定义API工具详细信息"""
        api_tool = await self.api_tool_service.get_api_tool(provider_id, tool_name)

        resp = GetApiToolResponse()

        return Response(
            code=HttpCode.SUCCESS,
            message="自定义API工具获取成功",
            data=resp.dump(api_tool)
        )

    async def create_api_tool(self, req: CreateApiToolRequest):
        """创建自定义API工具"""
        await self.api_tool_service.create_api_tool(req)

        return Response(
            code=HttpCode.SUCCESS,
            message="自定义API工具创建成功",
            data={}
        )

    async def get_api_tool_provider(self, provider_id: uuid.UUID):
        """获取自定义API工具供应商"""
        api_tool_provider = await self.api_tool_service.get_api_tool_provider(provider_id)

        resp = GetApiToolProviderResponse()

        return Response(
            code=HttpCode.SUCCESS,
            message="自定义API工具供应商获取成功",
            data=resp.dump(api_tool_provider)
        )

    async def delete_api_tool_provider(self, provider_id: uuid.UUID):
        """根据provider_id删除自定义API工具供应商信息"""
        await self.api_tool_service.delete_api_tool_provider(provider_id)

        return Response(
            code=HttpCode.SUCCESS,
            message="自定义API工具供应商删除成功",
            data={}
        )

    async def get_api_tool_providers_with_page(self, req: GetApiToolProvidersWithPageRequest):
        """获取API工具供应商列表信息，支持分页"""
        api_tool_providers, paginator = await self.api_tool_service.get_api_tool_providers_with_page(req)

        response_list = []
        for provider in api_tool_providers:
            resp = GetApiToolProvidersWithPageResponse(
                id=provider.id,
                name=provider.name,
                icon=provider.icon,
                openapi_schema=provider.openapi_schema,
                headers=[
                    {"key": item['key'], "value": item['value']}
                    for item in provider.headers
                ] if provider.headers else [],
                tools=[{
                    "id": tool.id,
                    "name": tool.name,
                    "description": tool.description,
                    "inputs": [{
                        k: v for k, v in parameter.items()if k != "in"
                    } for parameter in tool.parameters]
                } for tool in provider.tools],
                created_at=int(provider.created_at.timestamp()),
            )
            response_list.append(resp)

        return Response(
            code=HttpCode.SUCCESS,
            message="自定义API工具供应商列表获取成功",
            data=PageModel(
                data=response_list,
                paginator=paginator
            )
        )

    async def validate_openapi_schema(self, req: ValidateOpenApiSchemaRequest):
        """验证OpenAPI schema是否符合要求"""
        await self.api_tool_service.parse_openapi_schema(req.openapi_schema)

        return Response(
            code=HttpCode.SUCCESS,
            message="OpenAPI schema验证成功",
            data={}
        )

    async def update_api_tool_provider(self, provider_id: uuid.UUID, req: UpdateApiToolProviderRequest):
        """更新自定义API工具供应商"""
        await self.api_tool_service.update_api_tool_provider(provider_id, req)

        return Response(
            code=HttpCode.SUCCESS,
            message="自定义API工具供应商更新成功",
            data={}
        )
