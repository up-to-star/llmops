from pydantic import BaseModel, Field, HttpUrl
from marshmallow import Schema, fields, pre_dump
from internal.model import ApiToolProvider, ApiTool
from typing import Optional
from pkg.paginator import PaginatorRequest
import uuid


class ValidateOpenApiSchemaRequest(BaseModel):
    """验证OpenAPI schema是否符合要求"""
    openapi_schema: str = Field(
        ...,
        description="OpenAPI schema字符串",
        max_length=2048,
        json_schema_extra={
            "error_msg": {
                "missing": "openapi_schema is required",
                "max_length": "openapi_schema must be less than 2048 characters"
            }
        }
    )


class GetApiToolProvidersWithPageRequest(PaginatorRequest):
    """获取API工具供应商列表信息，支持分页"""
    search_word: Optional[str] = Field(
        default=None, description="搜索关键词，根据供应商名称或图标URL匹配")


class HeaderItem(BaseModel):
    """自定义API工具请求头项"""
    key: str = Field(..., description="header 键")
    value: str = Field(..., description="header 值")


class CreateApiToolRequest(BaseModel):
    """创建自定义API工具请求"""
    name: str = Field(..., description="自定义API工具名称",
                      min_length=1, max_length=30)
    icon: HttpUrl = Field(..., description="自定义API工具图标")
    openapi_schema: str = Field(..., description="自定义API工具OpenAPI schema")
    headers: list[HeaderItem] = Field(
        default_factory=list, description="请求头列表")


class GetApiToolProviderResponse(Schema):
    """获取自定义API工具供应商响应"""
    id = fields.UUID(attribute="id", description="自定义API工具供应商ID")
    name = fields.String(attribute="name", description="自定义API工具供应商名称")
    icon = fields.String(attribute="icon", description="自定义API工具供应商图标")
    openapi_schema = fields.String(
        attribute="openapi_schema", description="自定义API工具供应商OpenAPI schema")
    headers = fields.List(fields.Dict, default=[],
                          attribute="headers", description="请求头列表")
    created_at = fields.Integer(
        attribute="created_at", description="创建时间", default=0)

    @pre_dump
    def process_data(self, data: ApiToolProvider, **kwargs):
        return {
            "id": data.id,
            "name": data.name,
            "icon": data.icon,
            "openapi_schema": data.openapi_schema,
            "headers": data.headers,
            "created_at": int(data.created_at.timestamp()) if data.created_at else 0
        }


class GetApiToolProvidersWithPageResponse(BaseModel):
    """获取自定义API工具供应商列表信息，支持分页响应"""
    id: uuid.UUID = Field(description="自定义API工具供应商ID")
    name: str = Field(description="自定义API工具供应商名称")
    icon: str = Field(description="自定义API工具供应商图标")
    openapi_schema: str = Field(description="自定义API工具供应商OpenAPI schema")
    headers: list[HeaderItem] = Field(
        default_factory=list, description="请求头列表")
    tools: list = Field(default_factory=list, description="自定义API工具列表")
    created_at: int = Field(description="创建时间", default=0)


class GetApiToolResponse(Schema):
    """获取自定义API工具详细信息响应"""
    id = fields.UUID(attribute="id", description="自定义API工具ID")
    name = fields.String(attribute="name", description="自定义API工具名称")
    description = fields.String(
        attribute="description", description="自定义API工具描述")
    inputs = fields.List(fields.Dict, default=[],
                         attribute="inputs", description="输入参数列表")
    provider = fields.Dict(attribute="provider", description="供应商信息")

    @pre_dump
    def process_data(self, data: ApiTool, **kwargs):
        provider = data.provider
        return {
            "id": data.id,
            "name": data.name,
            "description": data.description,
            "inputs": [{k: v for k, v in parameter.items() if k != "in"} for parameter in data.parameters],
            "provider": {
                "id": provider.id,
                "name": provider.name,
                "icon": provider.icon,
                "description": provider.description,
                "headers": provider.headers
            }
        }


class UpdateApiToolProviderRequest(BaseModel):
    """更新自定义API工具供应商请求"""
    name: str = Field(..., description="自定义API工具名称",
                      min_length=1, max_length=30)
    icon: HttpUrl = Field(..., description="自定义API工具图标")
    openapi_schema: str = Field(..., description="自定义API工具OpenAPI schema")
    headers: list[HeaderItem] = Field(
        default_factory=list, description="请求头列表")

    
