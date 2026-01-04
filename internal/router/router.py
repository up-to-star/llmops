from fastapi import FastAPI, APIRouter
from internal.handle import AppHandler, BuiltinToolHandler, ApiToolHandler
from injector import inject
from pydantic import BaseModel
from internal.schema import CompletionRequest, ValidateOpenApiSchemaRequest, CreateApiToolRequest, GetApiToolProvidersWithPageRequest
import uuid


@inject
class AppRouter:
    """应用相关路由独立处理器"""
    app_handler: AppHandler

    def __init__(self, app_handler: AppHandler):
        self.app_handler = app_handler

    def get_router(self) -> APIRouter:
        """创建应用路由实例"""
        router = APIRouter(prefix="/apps")

        @router.get("/ping")
        async def ping():
            return await self.app_handler.ping()

        @router.post("/{app_id}/debug")
        async def debug(request: CompletionRequest, app_id: uuid.UUID):
            return await self.app_handler.debug(request.query, app_id)

        @router.get("/test_db")
        async def test_db():
            return await self.app_handler.test_db()

        @router.post("/")
        async def create_app():
            return await self.app_handler.create_app()

        @router.get("/{app_id}")
        async def get_app(app_id: uuid.UUID):
            return await self.app_handler.get_app(app_id)

        @router.put("/{app_id}")
        async def update_app(app_id: uuid.UUID):
            return await self.app_handler.update_app(app_id)

        @router.delete("/{app_id}")
        async def delete_app(app_id: uuid.UUID):
            return await self.app_handler.delete_app(app_id)

        return router


@inject
class BuiltinToolRouter:
    """内置工具路由独立处理器"""
    builtin_tool_handler: BuiltinToolHandler

    def __init__(self, builtin_tool_handler: BuiltinToolHandler):
        self.builtin_tool_handler = builtin_tool_handler

    def get_router(self) -> APIRouter:
        """创建内置工具路由实例"""
        router = APIRouter(prefix="/builtin-tools")

        @router.get("/")
        async def get_builtin_tools():
            return await self.builtin_tool_handler.get_builtin_tools()

        @router.get("/categories")
        async def get_categories():
            return await self.builtin_tool_handler.get_categories()

        @router.get("/{provider_name}/icon")
        async def get_provider_icon(provider_name: str):
            return await self.builtin_tool_handler.get_provider_icon(provider_name)

        @router.get("/{provider_name}/{tool_name}")
        async def get_provider_tool(provider_name: str, tool_name: str):
            return await self.builtin_tool_handler.get_provider_tool(provider_name, tool_name)

        return router


@inject
class ApiToolRouter:
    """API工具路由独立处理器"""
    api_tool_handler: ApiToolHandler

    def __init__(self, api_tool_handler: ApiToolHandler):
        self.api_tool_handler = api_tool_handler

    def get_router(self) -> APIRouter:
        """创建API工具路由实例"""
        router = APIRouter(prefix="/api-tools")

        @router.post("/validate-openapi-schema")
        async def validate_api_tool(request: ValidateOpenApiSchemaRequest):
            return await self.api_tool_handler.validate_openapi_schema(request)

        @router.post("/")
        async def create_api_tool(request: CreateApiToolRequest):
            return await self.api_tool_handler.create_api_tool(request)

        @router.get("/{provider_id}")
        async def get_api_tool_provider(provider_id: uuid.UUID):
            return await self.api_tool_handler.get_api_tool_provider(provider_id)

        @router.get("/{provider_id}/{tool_name}")
        async def get_api_tool(provider_id: uuid.UUID, tool_name: str):
            return await self.api_tool_handler.get_api_tool(provider_id, tool_name)

        @router.post("/{provider_id}/delete")
        async def delete_api_tool_provider(provider_id: uuid.UUID):
            return await self.api_tool_handler.delete_api_tool_provider(provider_id)

        @router.post("/pages")
        async def get_api_tool_providers_with_page(request: GetApiToolProvidersWithPageRequest):
            return await self.api_tool_handler.get_api_tool_providers_with_page(request)

        return router


@inject
class Router:
    """主路由器，统一管理所有独立的路由"""
    app_router: AppRouter
    builtin_tool_router: BuiltinToolRouter
    api_tool_router: ApiToolRouter

    def __init__(self,
                 app_router: AppRouter,
                 builtin_tool_router: BuiltinToolRouter,
                 api_tool_router: ApiToolRouter):
        self.app_router = app_router
        self.builtin_tool_router = builtin_tool_router
        self.api_tool_router = api_tool_router

    def register_routes(self, app: FastAPI):
        """注册所有独立的路由到FastAPI应用"""
        app.include_router(self.app_router.get_router())
        app.include_router(
            self.builtin_tool_router.get_router())
        app.include_router(self.api_tool_router.get_router())
